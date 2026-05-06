import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "name",        "label": "Donor ID",     "fieldtype": "Link",   "options": "Donor", "width": 140},
        {"fieldname": "donor_name",  "label": "Name",          "fieldtype": "Data",   "width": 160},
        {"fieldname": "blood_group", "label": "Blood Group",   "fieldtype": "Data",   "width": 100},
        {"fieldname": "status",      "label": "Status",        "fieldtype": "Data",   "width": 120},
        {"fieldname": "donor_type",  "label": "Type",          "fieldtype": "Data",   "width": 100},
        {"fieldname": "hospital",    "label": "Hospital",      "fieldtype": "Link",   "options": "Hospital", "width": 180},
        {"fieldname": "state",       "label": "State",         "fieldtype": "Data",   "width": 120},
        {"fieldname": "creation",    "label": "Registered On", "fieldtype": "Date",   "width": 120},
    ]


def get_data(filters):
    conditions = []
    values = {}

    if filters:
        if filters.get("status"):
            conditions.append("status = %(status)s")
            values["status"] = filters["status"]
        if filters.get("blood_group"):
            conditions.append("blood_group = %(blood_group)s")
            values["blood_group"] = filters["blood_group"]
        if filters.get("state"):
            conditions.append("state = %(state)s")
            values["state"] = filters["state"]
        if filters.get("from_date"):
            conditions.append("DATE(creation) >= %(from_date)s")
            values["from_date"] = filters["from_date"]
        if filters.get("to_date"):
            conditions.append("DATE(creation) <= %(to_date)s")
            values["to_date"] = filters["to_date"]

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    return frappe.db.sql(
        f"""
        SELECT name, donor_name, blood_group, status, donor_type, hospital, state,
               DATE(creation) AS creation
        FROM `tabDonor`
        {where}
        ORDER BY creation DESC
        """,
        values,
        as_dict=True,
    )
