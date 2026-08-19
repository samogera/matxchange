app_name = "matxchange"
app_title = "Matxchange"
app_publisher = "samogera"
app_description = "Operating System for circular economy"
app_email = "samuelohillary@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "matxchange",
# 		"logo": "/assets/matxchange/logo.png",
# 		"title": "Matxchange",
# 		"route": "/matxchange",
# 		"has_permission": "matxchange.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/matxchange/css/matxchange.css"
# app_include_js = "/assets/matxchange/js/matxchange.js"

# include js, css files in header of web template
# web_include_css = "/assets/matxchange/css/matxchange.css"
# web_include_js = "/assets/matxchange/js/matxchange.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "matxchange/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "matxchange/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "matxchange.utils.jinja_methods",
# 	"filters": "matxchange.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "matxchange.install.before_install"
# after_install = "matxchange.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "matxchange.uninstall.before_uninstall"
# after_uninstall = "matxchange.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "matxchange.utils.before_app_install"
# after_app_install = "matxchange.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "matxchange.utils.before_app_uninstall"
# after_app_uninstall = "matxchange.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "matxchange.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"matxchange.tasks.all"
# 	],
# 	"daily": [
# 		"matxchange.tasks.daily"
# 	],
# 	"hourly": [
# 		"matxchange.tasks.hourly"
# 	],
# 	"weekly": [
# 		"matxchange.tasks.weekly"
# 	],
# 	"monthly": [
# 		"matxchange.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "matxchange.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "matxchange.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "matxchange.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "matxchange.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["matxchange.utils.before_request"]
# after_request = ["matxchange.utils.after_request"]

# Job Events
# ----------
# before_job = ["matxchange.utils.before_job"]
# after_job = ["matxchange.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"matxchange.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []


# USSD Handler - Allow ngrok bypass
override_whitelisted_methods = {
    "matxchange.utils.ussd.handler": "matxchange.utils.ussd.handler"
}

fixtures = [
    {"dt": "DocType", "filters": [["module", "=", "Matxchange"]]},
    {"dt": "Custom Field", "filters": [["module", "=", "Matxchange"]]},
    {"dt": "Print Format", "filters": [["module", "=", "Matxchange"]]},
    {"dt": "Report", "filters": [["module", "=", "Matxchange"]]},
    {"dt": "Dashboard", "filters": [["module", "=", "Matxchange"]]},
    {"dt": "Dashboard Chart", "filters": [["module", "=", "Matxchange"]]},
    {"dt": "Notification", "filters": [["module", "=", "Matxchange"]]},
    {"dt": "Number Card", "filters": [["module", "=", "Matxchange"]]},
    {"dt": "Email Template", "filters": [["name", "in", ["welcome-matxchange", "payment-confirmed", "transaction-submitted"]]]},
    {"dt": "Workspace", "filters": [["name", "in", ["MatXchange"]]]},
]

# Add this to the bottom of matxchange/hooks.py
#
# Frappe serves its own login and signup pages at /login and /signup, and
# redirects any logged-out visitor there. These rules send those visitors
# to the Matxchange pages instead, so nobody ever sees Frappe's version.
#
# WARNING: once this is live, https://app.matxchange.co.ke/login no longer
# works as an escape hatch. If your custom login page ever breaks you would
# be locked out of the desk. Two ways back in:
#   1. Comment these lines out and run: bench restart
#   2. Reset the admin password from the server:
#      bench --site matxchange.co.ke set-admin-password <newpassword>
#
# Test that matxchange.co.ke/Login.dc.html logs you in successfully BEFORE
# adding this.

website_redirects = [
    {
        "source": "/login",
        "target": "https://matxchange.co.ke/Login.dc.html",
    },
    {
        "source": "/signup",
        "target": "https://matxchange.co.ke/Signup.dc.html",
    },
]
