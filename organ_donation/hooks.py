from . import __version__ as app_version

app_name = "organ_donation"
app_title = "Organ Donation Trust"
app_publisher = "Mohan Foundation"
app_description = "Organ Donation Management System for ERPNext v15+"
app_email = "support@organdonation.org"
app_license = "MIT"

# ------------------------------------------------------------
# Fixtures – exported with `bench export-fixtures`
# ------------------------------------------------------------
fixtures = [
    "Custom Field",
    "Property Setter",
    "Notification",
    "Workflow",
    "Workflow State",
    "Workflow Action Master",
    "Web Form",
    "Report",
    "Print Format",
    "Letter Head",
    "Role",
    "Custom Role",
]

# ------------------------------------------------------------
# DocType Events
# ------------------------------------------------------------
doc_events = {
    "Donor": {
        "after_insert": "organ_donation.api.patient_sync.create_patient_from_donor",
        "on_update":    "organ_donation.api.notifications.notify_donor_status_change",
    },
    "Organ Match": {
        "on_submit":    "organ_donation.api.matching.on_match_submit",
        "on_update":    "organ_donation.api.notifications.notify_match_update",
    },
    "Brain Death Certificate": {
        "on_submit":    "organ_donation.api.patient_sync.mark_donor_brain_dead",
    },
    "Family Consent": {
        "on_submit":    "organ_donation.api.patient_sync.record_family_consent",
    },
}

# ------------------------------------------------------------
# Scheduled Tasks
# ------------------------------------------------------------
scheduler_events = {
    "daily": [
        "organ_donation.tasks.daily.send_waitlist_digest",
        "organ_donation.tasks.daily.expire_old_pledges",
    ],
    "hourly": [
        "organ_donation.tasks.hourly.check_critical_recipients",
    ],
}

# ------------------------------------------------------------
# Permissions
# ------------------------------------------------------------
# Roles defined: Organ Donation Manager, Transplant Coordinator,
#                Hospital Admin, Donor (Portal)

# ------------------------------------------------------------
# Website / Portal
# ------------------------------------------------------------
website_route_rules = [
    {"from_route": "/donor-registration", "to_route": "donor_registration"},
    {"from_route": "/recipient-registration", "to_route": "recipient_registration"},
]

portal_menu_items = [
    {"title": "My Donor Profile",   "route": "/donor-registration",    "reference_doctype": "Donor"},
    {"title": "Organ Pledge",       "route": "/organ-pledge",          "reference_doctype": "Organ Pledge"},
]

# ------------------------------------------------------------
# Email / Notification
# ------------------------------------------------------------
standard_queries = {
    "Donor": "organ_donation.api.queries.donor_query",
}

# ------------------------------------------------------------
# Override standard doctypes (ERPNext Healthcare integration)
# ------------------------------------------------------------
override_doctype_class = {}

# ------------------------------------------------------------
# Boot session
# ------------------------------------------------------------
boot_session = "organ_donation.api.boot.boot_session"

# ------------------------------------------------------------
# On app install
# ------------------------------------------------------------
after_install = "organ_donation.setup.install.after_install"
after_migrate = "organ_donation.setup.install.after_migrate"
