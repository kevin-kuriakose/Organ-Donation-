import frappe


def find_match(organ):
    """Return potential recipients and available donors for a given organ."""
    recipients = frappe.get_all(
        "Recipient",
        filters={"required_organ": organ, "status": "Waiting"},
        fields=["name", "patient_name", "blood_group", "urgency", "waitlist_date"],
        order_by="urgency desc, waitlist_date asc",
    )
    donors = frappe.get_all(
        "Organ Pledge",
        filters={"organ": organ, "pledge_status": "Active", "docstatus": 1},
        fields=["name", "donor", "pledge_date"],
    )
    return {"recipients": recipients, "donors": donors}


@frappe.whitelist()
def auto_match(organ):
    """
    Whitelist API – find compatible donor/recipient pairs for an organ and
    create draft Organ Match documents.
    Called from the Workspace dashboard button.
    """
    result = find_match(organ)
    matches_created = []

    for pledge in result["donors"]:
        donor_bg = frappe.db.get_value("Donor", pledge["donor"], "blood_group")
        donor_status = frappe.db.get_value("Donor", pledge["donor"], "status")
        if donor_status not in ("Brain Dead", "Consented"):
            continue
        for recipient in result["recipients"]:
            if _is_blood_group_compatible(donor_bg, recipient["blood_group"]):
                existing = frappe.db.exists(
                    "Organ Match",
                    {"donor": pledge["donor"], "recipient": recipient["name"], "status": ["!=", "Rejected"]},
                )
                if not existing:
                    match_doc = frappe.get_doc({
                        "doctype": "Organ Match",
                        "organ": organ,
                        "donor": pledge["donor"],
                        "recipient": recipient["name"],
                        "match_date": frappe.utils.now(),
                        "status": "Proposed",
                    })
                    match_doc.insert(ignore_permissions=True)
                    matches_created.append(match_doc.name)
                break  # one recipient per donor organ

    frappe.db.commit()
    return {"matches_created": matches_created, "count": len(matches_created)}


def on_match_submit(doc, method):
    """Hook called when an Organ Match is submitted."""
    frappe.db.set_value("Recipient", doc.recipient, "status", "Matched")
    frappe.db.set_value("Donor", doc.donor, "status", "Organ Harvested")


def _is_blood_group_compatible(donor_bg, recipient_bg):
    compatibility = {
        "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
        "O+": ["O+", "A+", "B+", "AB+"],
        "A-": ["A-", "A+", "AB-", "AB+"],
        "A+": ["A+", "AB+"],
        "B-": ["B-", "B+", "AB-", "AB+"],
        "B+": ["B+", "AB+"],
        "AB-": ["AB-", "AB+"],
        "AB+": ["AB+"],
    }
    return recipient_bg in compatibility.get(donor_bg, [])
