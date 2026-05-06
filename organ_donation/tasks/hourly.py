import frappe


def check_critical_recipients():
    """Alert coordinators if there are Super Urgent recipients with no proposed match."""
    critical = frappe.db.sql(
        """
        SELECT r.name, r.patient_name, r.required_organ
        FROM `tabRecipient` r
        LEFT JOIN `tabOrgan Match` om
            ON om.recipient = r.name AND om.status NOT IN ('Rejected', 'Failed')
        WHERE r.status = 'Waiting'
          AND r.urgency = 'Super Urgent'
          AND om.name IS NULL
        """,
        as_dict=True,
    )
    if not critical:
        return
    rows = "".join(
        f"<tr><td>{r.name}</td><td>{r.patient_name}</td><td>{r.required_organ}</td></tr>"
        for r in critical
    )
    message = f"""
    <p>⚠️ The following <strong>Super Urgent</strong> recipients have <strong>no active match</strong>:</p>
    <table border="1" cellpadding="4">
      <tr><th>ID</th><th>Patient</th><th>Organ Needed</th></tr>
      {rows}
    </table>
    <p>Please initiate matching immediately.</p>
    """
    coordinators = frappe.get_all(
        "Has Role", filters={"role": "Transplant Coordinator"}, fields=["parent"]
    )
    for c in coordinators:
        frappe.sendmail(
            recipients=[c.parent],
            subject="🚨 [Organ Donation] Unmatched Super Urgent Recipients",
            message=message,
        )
