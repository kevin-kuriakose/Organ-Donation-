import frappe
from frappe.model.document import Document


class OrganMatch(Document):

    def validate(self):
        self._check_blood_group()

    def _check_blood_group(self):
        donor_bg = frappe.db.get_value("Donor", self.donor, "blood_group")
        recipient_bg = frappe.db.get_value("Recipient", self.recipient, "blood_group")
        compatible = self._is_blood_group_compatible(donor_bg, recipient_bg)
        self.blood_group_match = 1 if compatible else 0
        if not compatible:
            frappe.msgprint(
                f"⚠️ Blood group mismatch: Donor {donor_bg} → Recipient {recipient_bg}. "
                "Please verify before proceeding.",
                alert=True,
                indicator="orange",
            )

    @staticmethod
    def _is_blood_group_compatible(donor, recipient):
        compatibility = {
            "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
            "O+": ["O+", "A+", "B+", "AB+"],
            "A-": ["A-", "A+", "AB-", "AB+"],
            "A+": ["A+", "AB+"],
            "B-": ["B-", "B+", "AB-", "AB+"],
            "B+": ["B+", "AB+"],
            "AB-": ["AB-", "AB+"],
            "AB+": ["AB+"],
        }
        return recipient in compatibility.get(donor, [])

    def on_submit(self):
        frappe.db.set_value("Recipient", self.recipient, "status", "Matched")
        frappe.db.set_value("Donor", self.donor, "status", "Organ Harvested")

    def on_cancel(self):
        frappe.db.set_value("Recipient", self.recipient, "status", "Waiting")
