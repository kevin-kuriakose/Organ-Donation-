import frappe
from frappe.model.document import Document


class FamilyConsent(Document):

    def on_submit(self):
        if self.consent_given == "Yes":
            frappe.db.set_value("Donor", self.donor, "status", "Consented")
            frappe.msgprint("Family consent recorded. Organ harvesting can now be coordinated.")
        elif self.consent_given == "No":
            frappe.db.set_value("Donor", self.donor, "status", "Withdrawn")
            frappe.msgprint("Family has refused consent. Donor status updated.")
