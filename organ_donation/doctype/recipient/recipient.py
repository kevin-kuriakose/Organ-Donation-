import frappe
from frappe.model.document import Document
from frappe.utils import today


class Recipient(Document):

    def validate(self):
        if not self.waitlist_date:
            self.waitlist_date = today()

    def on_update(self):
        if self.status == "Matched":
            frappe.publish_realtime(
                "organ_match_update",
                {"recipient": self.name, "status": "Matched"},
                user=frappe.session.user,
            )
