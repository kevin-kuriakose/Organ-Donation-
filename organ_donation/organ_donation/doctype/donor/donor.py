import frappe
from frappe.model.document import Document
from frappe.utils import today


class Donor(Document):

    def validate(self):
        self._validate_aadhaar()
        self._validate_age()

    def before_insert(self):
        if not self.registered_by:
            self.registered_by = frappe.session.user

    def _validate_aadhaar(self):
        if self.aadhaar and len(self.aadhaar) not in (12, 0):
            frappe.throw("Aadhaar number must be 12 digits.")

    def _validate_age(self):
        if self.date_of_birth:
            from frappe.utils import date_diff, getdate
            age = date_diff(today(), self.date_of_birth) // 365
            if age < 5:
                frappe.throw("Donor must be at least 5 years old.")

    def on_update(self):
        # Keep linked Patient in sync if Healthcare module present
        try:
            if frappe.db.exists("Patient", {"patient_name": self.donor_name}):
                frappe.db.set_value(
                    "Patient", {"patient_name": self.donor_name},
                    "blood_group", self.blood_group
                )
        except Exception:
            pass
