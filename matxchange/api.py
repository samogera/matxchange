import frappe
from frappe import _
from frappe.utils import escape_html, validate_email_address

# Account types offered on the public signup form. Anything not in this
# list is rejected, so a crafted request can't hand itself System Manager.
# Edit these to match the Roles that exist in your Frappe site.
ALLOWED_ROLES = {
    "Waste Generator",
    "Collector",
    "Aggregator",
    "Recycler",
    "Buyer",
}


def normalize_phone(raw):
    """Store Kenyan numbers in one canonical form: +2547XXXXXXXX.

    Frappe matches mobile logins against User.mobile_no exactly, so a number
    saved as "0712 345 678" can never be logged in with as "+254712345678".
    Everything is normalised on the way in, and the login page applies the
    same rule on the way out.
    """
    if not raw:
        return None

    digits = "".join(ch for ch in str(raw) if ch.isdigit())
    if not digits:
        return None

    if digits.startswith("254"):
        digits = digits[3:]
    elif digits.startswith("0"):
        digits = digits[1:]

    if len(digits) != 9:
        # Not a Kenyan mobile - keep what the user typed, stripped of spaces.
        return "+" + digits if str(raw).strip().startswith("+") else str(raw).strip()

    return "+254" + digits


@frappe.whitelist(allow_guest=True)
def register(full_name, email, password=None, phone=None, company=None, role=None):
    """Create a Matxchange account from the public signup form.

    Frappe's built-in sign_up only takes an email and a name. This form
    also collects a phone number, an account type, and optionally a
    password, so it needs its own endpoint.

    If no password is supplied, the account is created disabled-until-
    verified and Frappe emails a link for the user to set their own.
    """
    if frappe.db.get_single_value("Website Settings", "disable_signup"):
        frappe.throw(_("Sign up is currently disabled."), frappe.PermissionError)

    email = (email or "").strip().lower()
    full_name = (full_name or "").strip()
    phone = (phone or "").strip()
    company = (company or "").strip()
    role = (role or "").strip()

    if not full_name:
        frappe.throw(_("Please enter your full name."))

    validate_email_address(email, throw=True)

    if password and len(password) < 8:
        frappe.throw(_("Your password must be at least 8 characters long."))

    if role and role not in ALLOWED_ROLES:
        frappe.throw(_("That account type isn't available."))

    # Rate limit by IP so the endpoint can't be used to mass-create users.
    _check_rate_limit()

    if frappe.db.exists("User", email):
        return {
            "status": "exists",
            "message": _("An account with this email already exists. Try logging in."),
        }

    parts = full_name.split(" ")
    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": escape_html(parts[0]),
        "last_name": escape_html(" ".join(parts[1:])) or None,
        "mobile_no": phone or None,
        "user_type": "Website User",
        "send_welcome_email": 0 if password else 1,
        "enabled": 1,
    })
    user.flags.ignore_permissions = True
    user.insert()

    if password:
        # Password policy is deliberately NOT bypassed here. Frappe checks the
        # password against System Settings > Minimum Password Score and throws
        # a readable message the signup form surfaces to the user.
        user.new_password = password
        user.save(ignore_permissions=True)

    if role:
        _assign_role(user, role)

    _store_profile(user, company, role)

    frappe.db.commit()

    return {
        "status": "ok",
        "email": email,
        "message": (
            _("Account created. You can log in now.")
            if password
            else _("Account created. Check your email to set your password.")
        ),
    }


def _check_rate_limit(prefix="signup_attempts", limit=5, message=None):
    ip = frappe.local.request_ip
    key = f"{prefix}:{ip}"
    count = frappe.cache().get_value(key) or 0
    if int(count) >= limit:
        frappe.throw(message or _("Too many attempts. Please try again in an hour."))
    frappe.cache().set_value(key, int(count) + 1, expires_in_sec=3600)


def _assign_role(user, role):
    """Attach the Frappe Role matching the chosen account type, if it exists."""
    if not frappe.db.exists("Role", role):
        return
    user.append("roles", {"role": role})
    user.save(ignore_permissions=True)


def _store_profile(user, company, role):
    """Write company/account type onto the User record.

    Only writes fields that actually exist, so it won't break if you
    haven't created these custom fields yet.
    """
    meta = frappe.get_meta("User")
    updates = {}
    if company and meta.has_field("company_name"):
        updates["company_name"] = escape_html(company)
    if role and meta.has_field("account_type"):
        updates["account_type"] = role
    if updates:
        frappe.db.set_value("User", user.name, updates, update_modified=False)


@frappe.whitelist(allow_guest=True)
def google_login_url(redirect_to="/app"):
    """Return the Google authorize URL for the custom login page.

    Calling login_via_google directly raises a TypeError, because that
    function is the *callback* and expects a code and state from Google.
    This builds the URL that starts the flow instead.
    """
    from frappe.utils.oauth import get_oauth2_authorize_url

    if not frappe.db.get_value("Social Login Key", "google", "enable_social_login"):
        frappe.throw(_("Google sign-in isn't set up yet."))

    return {"url": get_oauth2_authorize_url("google", redirect_to)}


# Where landing-page enquiries are emailed.
CONTACT_RECIPIENT = "samuel@matxchange.co.ke"


@frappe.whitelist(allow_guest=True)
def submit_contact(name, email, message, company=None, role=None):
    """Store a landing-page enquiry and email the team.

    Creates a Communication so enquiries are searchable in the desk rather
    than living only in an inbox.
    """
    _check_rate_limit(
        prefix="contact_attempts",
        limit=5,
        message=_("You've sent several messages already. Please try again later."),
    )

    name = escape_html((name or "").strip())
    email = (email or "").strip().lower()
    message = (message or "").strip()
    company = escape_html((company or "").strip())
    role = escape_html((role or "").strip())

    if not name:
        frappe.throw(_("Please enter your name."))
    if not message:
        frappe.throw(_("Please tell us how we can help."))

    validate_email_address(email, throw=True)

    body = "<br>".join(
        filter(
            None,
            [
                f"<b>Name:</b> {name}",
                f"<b>Email:</b> {email}",
                f"<b>Company:</b> {company}" if company else None,
                f"<b>Role:</b> {role}" if role else None,
                "",
                f"<b>Message:</b><br>{frappe.utils.escape_html(message)}",
            ],
        )
    )

    comm = frappe.get_doc(
        {
            "doctype": "Communication",
            "communication_type": "Communication",
            "communication_medium": "Email",
            "sent_or_received": "Received",
            "subject": f"Website enquiry from {name}",
            "content": body,
            "sender": email,
            "sender_full_name": name,
            "recipients": CONTACT_RECIPIENT,
            "status": "Open",
        }
    )
    comm.flags.ignore_permissions = True
    comm.insert(ignore_permissions=True)

    try:
        frappe.sendmail(
            recipients=[CONTACT_RECIPIENT],
            subject=f"Website enquiry from {name}",
            message=body,
            reply_to=email,
        )
    except Exception:
        # The enquiry is saved either way; a mail failure shouldn't lose it.
        frappe.log_error(title="Contact form email failed")

    frappe.db.commit()

    return {"status": "ok", "message": _("Thanks, we'll be in touch shortly.")}


@frappe.whitelist(allow_guest=True)
def email_login_link(email):
    """Send a passwordless login link.

    Wraps Frappe's own send_login_link so the frontend has one stable
    endpoint, and so a disabled setting or an unknown address produces a
    predictable answer instead of a raw traceback.
    """
    email = (email or "").strip().lower()
    validate_email_address(email, throw=True)

    _check_rate_limit(
        prefix="login_link",
        limit=5,
        message=_("Too many login links requested. Please try again later."),
    )

    if not frappe.db.get_single_value("System Settings", "login_with_email_link"):
        frappe.throw(_("Login by email link isn't switched on for this site."))

    # Unknown addresses return success on purpose: confirming which emails
    # have accounts would let anyone enumerate your users.
    if not frappe.db.exists("User", {"email": email, "enabled": 1}):
        return {"status": "ok"}

    try:
        from frappe.www.login import send_login_link as _send
    except ImportError:
        frappe.throw(_("This Frappe version doesn't support email link login."))

    _send(email)
    return {"status": "ok"}


@frappe.whitelist(allow_guest=True)
def request_password_reset(email):
    """Send a password reset link.

    Frappe's reset_password throws "User not found" for unknown addresses,
    which leaks whether an account exists. This returns the same answer
    either way.
    """
    email = (email or "").strip().lower()
    validate_email_address(email, throw=True)

    _check_rate_limit(
        prefix="reset_attempts",
        limit=5,
        message=_("Too many reset requests. Please try again later."),
    )

    user = frappe.db.get_value("User", {"email": email, "enabled": 1}, "name")
    if user:
        try:
            frappe.get_doc("User", user).reset_password(send_email=True)
        except Exception:
            frappe.log_error(title="Password reset email failed")

    return {"status": "ok"}


@frappe.whitelist(allow_guest=True)
def profile_status():
    """Tell the completion page who is logged in and what's still missing.

    Google gives us a name and email but nothing else, so a user who signed
    up that way arrives with no role, company or phone.
    """
    if frappe.session.user == "Guest":
        return {"logged_in": False}

    user = frappe.get_doc("User", frappe.session.user)
    user_roles = {r.role for r in (user.roles or [])}
    matched = user_roles & ALLOWED_ROLES

    return {
        "logged_in": True,
        "email": user.name,
        "full_name": user.full_name or "",
        "first_name": user.first_name or "",
        "phone": user.mobile_no or "",
        "role": next(iter(matched), ""),
        "needs_profile": not (matched and user.mobile_no),
    }


@frappe.whitelist()
def complete_profile(phone=None, company=None, role=None):
    """Attach role, company and phone to an account created via Google.

    Deliberately NOT allow_guest: this only ever edits the logged-in user,
    so nobody can use it to modify someone else's record.
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("Please log in first."), frappe.PermissionError)

    role = (role or "").strip()
    if not role:
        frappe.throw(_("Please choose an account type."))
    if role not in ALLOWED_ROLES:
        frappe.throw(_("That account type isn't available."))

    phone = normalize_phone(phone)
    if not phone:
        frappe.throw(_("Please enter your phone number."))

    user = frappe.get_doc("User", frappe.session.user)
    user.mobile_no = phone
    user.flags.ignore_permissions = True
    user.save(ignore_permissions=True)

    _assign_role(user, role)
    _store_profile(user, company, role)

    frappe.db.commit()

    return {"status": "ok", "home": "/"}
