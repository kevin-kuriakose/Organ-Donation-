import frappe
from frappe.model.document import Document


class OrganPledge(Document):

    def validate(self):
        if not self.consent_given:
            frappe.throw("Donor must give informed consent before a pledge can be saved.")

    def on_submit(self):
        frappe.db.set_value("Donor", self.donor, "status", "Pledged")
        frappe.msgprint(f"Organ Pledge {self.name} submitted. Donor status updated to Pledged.")

    def on_cancel(self):
        frappe.db.set_value("Donor", self.donor, "status", "Withdrawn")
