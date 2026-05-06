
import frappe

def find_match(organ):
    recipients = frappe.get_all("Recipient", filters={"required_organ": organ})
    donors = frappe.get_all("Organ Pledge", filters={"organ": organ})
    return {"recipients": recipients, "donors": donors}
