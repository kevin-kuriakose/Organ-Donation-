import frappe
from frappe.model.document import Document


class TransplantLog(Document):

    def on_submit(self):
        if self.outcome == "Successful":
            frappe.db.set_value("Recipient", self.recipient, "status", "Transplanted")
            frappe.db.set_value(
                "Organ Match", self.organ_match, "status", "Transplanted"
            )
        elif self.outcome == "Failed":
            frappe.db.set_value("Recipient", self.recipient, "status", "Waiting")
            frappe.db.set_value(
                "Organ Match", self.organ_match, "status", "Failed"
            )
