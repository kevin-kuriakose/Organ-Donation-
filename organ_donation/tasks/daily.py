import frappe
from frappe.utils import today, add_days


def send_waitlist_digest():
    """Send a daily summary of the waiting list to Organ Donation Managers."""
    waiting = frappe.db.count("Recipient", {"status": "Waiting"})
    super_urgent = frappe.db.count("Recipient", {"status": "Waiting", "urgency": "Super Urgent"})
    managers = frappe.get_all(
        "Has Role", filters={"role": "Organ Donation Manager"}, fields=["parent"]
    )
    if not managers:
        return
    message = f"""
    <h3>Daily Organ Donation Waiting List Digest – {today()}</h3>
    <ul>
        <li>Total Recipients Waiting: <strong>{waiting}</strong></li>
        <li>Super Urgent Cases: <strong>{super_urgent}</strong></li>
    </ul>
    <p>Please log in to review and act on pending matches.</p>
    """
    for mgr in managers:
        frappe.sendmail(
            recipients=[mgr.parent],
            subject=f"[Organ Donation] Daily Waiting List Digest – {today()}",
            message=message,
        )


def expire_old_pledges():
    """Mark pledges older than 10 years as expired."""
    expiry_date = add_days(today(), -3650)
    frappe.db.sql(
        """
        UPDATE `tabOrgan Pledge`
        SET pledge_status = 'Expired'
        WHERE pledge_status = 'Active' AND pledge_date < %s AND docstatus = 1
        """,
        expiry_date,
    )
    frappe.db.commit()
