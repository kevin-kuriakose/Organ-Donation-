import frappe
from frappe.model.document import Document


class BrainDeathCertificate(Document):

    def validate(self):
        if self.apnea_test_done and not self.apnea_test_result:
            frappe.throw("Please enter Apnea Test Result.")

    def on_submit(self):
        frappe.db.set_value("Donor", self.donor, "status", "Brain Dead")
        frappe.msgprint(
            f"Brain Death certified for Donor {self.donor}. "
            "Family Consent process can now be initiated."
        )
        # Trigger notification to Transplant Coordinator
        frappe.publish_realtime(
            "brain_death_certified",
            {"donor": self.donor, "certificate": self.name},
        )
