import frappe


def create_patient_from_donor(doc, method):
    """
    After a Donor is inserted, create a linked Patient record in the
    ERPNext Healthcare module (if installed).
    """
    try:
        if not frappe.db.table_exists("tabPatient"):
            return
        if not frappe.db.exists("Patient", {"patient_name": doc.donor_name}):
            patient = frappe.get_doc({
                "doctype": "Patient",
                "patient_name": doc.donor_name,
                "blood_group": doc.blood_group,
                "sex": doc.gender or "Male",
                "mobile": doc.mobile or "",
                "email": doc.email or "",
            })
            patient.insert(ignore_permissions=True)
            frappe.db.commit()
    except Exception as e:
        frappe.log_error(str(e), "Patient Sync from Donor")


def mark_donor_brain_dead(doc, method):
    """When a Brain Death Certificate is submitted, update Donor status."""
    if frappe.db.exists("Donor", doc.donor):
        frappe.db.set_value("Donor", doc.donor, "status", "Brain Dead")


def record_family_consent(doc, method):
    """When Family Consent is submitted, update donor status accordingly."""
    if doc.consent_given == "Yes":
        frappe.db.set_value("Donor", doc.donor, "status", "Consented")
    elif doc.consent_given == "No":
        frappe.db.set_value("Donor", doc.donor, "status", "Withdrawn")
