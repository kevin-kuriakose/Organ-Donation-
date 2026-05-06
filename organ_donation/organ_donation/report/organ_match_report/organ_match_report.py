import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart


def get_columns():
    return [
        {"fieldname": "name",             "label": "Match ID",      "fieldtype": "Link",  "options": "Organ Match", "width": 140},
        {"fieldname": "organ",            "label": "Organ",         "fieldtype": "Data",  "width": 120},
        {"fieldname": "donor",            "label": "Donor",         "fieldtype": "Link",  "options": "Donor",       "width": 140},
        {"fieldname": "recipient",        "label": "Recipient",     "fieldtype": "Link",  "options": "Recipient",   "width": 140},
        {"fieldname": "donor_hospital",   "label": "Donor Hospital","fieldtype": "Link",  "options": "Hospital",    "width": 160},
        {"fieldname": "status",           "label": "Status",        "fieldtype": "Data",  "width": 110},
        {"fieldname": "blood_group_match","label": "BG Compatible", "fieldtype": "Check", "width": 100},
        {"fieldname": "hla_match_score",  "label": "HLA Score",     "fieldtype": "Float", "width": 90},
        {"fieldname": "match_date",       "label": "Match Date",    "fieldtype": "Datetime","width": 150},
    ]


def get_data(filters):
    conditions = []
    values = {}
    if filters:
        if filters.get("organ"):
            conditions.append("organ = %(organ)s")
            values["organ"] = filters["organ"]
        if filters.get("status"):
            conditions.append("status = %(status)s")
            values["status"] = filters["status"]
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    return frappe.db.sql(
        f"""
        SELECT name, organ, donor, recipient, donor_hospital, status,
               blood_group_match, hla_match_score, match_date
        FROM `tabOrgan Match`
        {where}
        ORDER BY match_date DESC
        """,
        values,
        as_dict=True,
    )


def get_chart(data):
    status_counts = {}
    for row in data:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    return {
        "data": {
            "labels": list(status_counts.keys()),
            "datasets": [{"values": list(status_counts.values())}],
        },
        "type": "donut",
        "title": "Organ Match by Status",
    }
