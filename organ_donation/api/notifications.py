import frappe
from frappe.utils import get_url_to_form


def notify_donor_status_change(doc, method):
    """Notify the Transplant Coordinator when a Donor's status changes."""
    if doc.has_value_changed("status"):
        coordinators = frappe.get_all(
            "Has Role",
            filters={"role": "Transplant Coordinator"},
            fields=["parent"],
        )
        for c in coordinators:
            frappe.sendmail(
                recipients=[c.parent],
                subject=f"[Organ Donation] Donor {doc.donor_name} – Status: {doc.status}",
                message=f"""
                <p>Dear Coordinator,</p>
                <p>Donor <strong>{doc.donor_name}</strong> ({doc.name}) status has changed to
                <strong>{doc.status}</strong>.</p>
                <p><a href="{get_url_to_form('Donor', doc.name)}">View Donor Record</a></p>
                """,
                now=True,
            )


def notify_match_update(doc, method):
    """Notify when Organ Match status changes."""
    if doc.has_value_changed("status") and doc.status in ("Approved", "Rejected"):
        subject = f"[Organ Donation] Organ Match {doc.name} – {doc.status}"
        message = f"""
        <p>Organ Match <strong>{doc.name}</strong> has been
        <strong>{doc.status}</strong>.</p>
        <p>Organ: {doc.organ} | Donor: {doc.donor} | Recipient: {doc.recipient}</p>
        <p><a href="{get_url_to_form('Organ Match', doc.name)}">View Match</a></p>
        """
        coordinators = frappe.get_all(
            "Has Role",
            filters={"role": "Transplant Coordinator"},
            fields=["parent"],
        )
        for c in coordinators:
            frappe.sendmail(recipients=[c.parent], subject=subject, message=message, now=True)
