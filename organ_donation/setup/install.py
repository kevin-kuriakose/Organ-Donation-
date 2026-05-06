import frappe


def after_install():
    """Run after `bench install-app organ_donation`."""
    create_roles()
    create_custom_fields()
    frappe.db.commit()
    print("✅ Organ Donation Trust installed successfully.")


def after_migrate():
    """Run after `bench migrate`."""
    create_custom_fields()
    frappe.db.commit()


def create_roles():
    roles = [
        "Organ Donation Manager",
        "Transplant Coordinator",
        "Hospital Admin",
    ]
    for role_name in roles:
        if not frappe.db.exists("Role", role_name):
            role = frappe.get_doc({"doctype": "Role", "role_name": role_name})
            role.insert(ignore_permissions=True)
            print(f"  Created role: {role_name}")


def create_custom_fields():
    """
    Example: add a custom field to ERPNext Patient linking back to Donor.
    Only runs if the Healthcare module (Patient doctype) is present.
    """
    try:
        if not frappe.db.table_exists("tabPatient"):
            return
        if not frappe.db.exists("Custom Field", "Patient-organ_donor_id"):
            cf = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Patient",
                "fieldname": "organ_donor_id",
                "fieldtype": "Link",
                "options": "Donor",
                "label": "Organ Donor ID",
                "insert_after": "patient_name",
                "module": "Organ Donation",
            })
            cf.insert(ignore_permissions=True)
            print("  Created custom field: Patient.organ_donor_id")
    except Exception as e:
        print(f"  Custom field creation skipped: {e}")
