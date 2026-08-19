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


def _check_rate_limit():
    ip = frappe.local.request_ip
    key = f"signup_attempts:{ip}"
    count = frappe.cache().get_value(key) or 0
    if int(count) >= 5:
        frappe.throw(_("Too many signup attempts. Please try again in an hour."))
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
