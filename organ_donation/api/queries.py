import frappe


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def donor_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
        f"""
        SELECT name, donor_name, blood_group, status
        FROM `tabDonor`
        WHERE ({searchfield} LIKE %(txt)s OR donor_name LIKE %(txt)s)
        LIMIT %(page_len)s OFFSET %(start)s
        """,
        {"txt": f"%{txt}%", "page_len": page_len, "start": start},
    )


@frappe.whitelist()
def get_dashboard_stats():
    """Return key metrics for the Workspace dashboard."""
    return {
        "total_donors": frappe.db.count("Donor"),
        "active_pledges": frappe.db.count("Organ Pledge", {"pledge_status": "Active"}),
        "waiting_recipients": frappe.db.count("Recipient", {"status": "Waiting"}),
        "successful_transplants": frappe.db.count("Transplant Log", {"outcome": "Successful"}),
        "pending_matches": frappe.db.count("Organ Match", {"status": "Proposed"}),
    }
