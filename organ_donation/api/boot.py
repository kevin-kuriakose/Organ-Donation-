import frappe


def boot_session(bootinfo):
    """Add organ donation stats to the boot session for dashboard widgets."""
    if frappe.session.user != "Guest":
        try:
            bootinfo.organ_donation_stats = {
                "waiting_recipients": frappe.db.count("Recipient", {"status": "Waiting"}),
                "pending_matches": frappe.db.count("Organ Match", {"status": "Proposed"}),
            }
        except Exception:
            pass
