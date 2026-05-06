
import frappe

def create_patient_from_donor(doc, method):
    if not frappe.db.exists("Patient", doc.donor_name):
        patient = frappe.get_doc({
            "doctype": "Patient",
            "patient_name": doc.donor_name,
            "blood_group": doc.blood_group
        })
        patient.insert(ignore_permissions=True)
