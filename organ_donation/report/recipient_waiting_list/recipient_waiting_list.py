import frappe
from frappe.utils import date_diff, today


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart


def get_columns():
    return [
        {"fieldname": "name",          "label": "Recipient ID",   "fieldtype": "Link", "options": "Recipient", "width": 140},
        {"fieldname": "patient_name",  "label": "Patient Name",   "fieldtype": "Data", "width": 160},
        {"fieldname": "required_organ","label": "Required Organ", "fieldtype": "Data", "width": 130},
        {"fieldname": "blood_group",   "label": "Blood Group",    "fieldtype": "Data", "width": 100},
        {"fieldname": "urgency",       "label": "Urgency",        "fieldtype": "Data", "width": 110},
        {"fieldname": "hospital",      "label": "Hospital",       "fieldtype": "Link", "options": "Hospital", "width": 160},
        {"fieldname": "waitlist_date", "label": "Waitlist Date",  "fieldtype": "Date", "width": 120},
        {"fieldname": "days_waiting",  "label": "Days Waiting",   "fieldtype": "Int",  "width": 110},
        {"fieldname": "status",        "label": "Status",         "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    conditions = ["status = 'Waiting'"]
    values = {}
    if filters:
        if filters.get("required_organ"):
            conditions.append("required_organ = %(required_organ)s")
            values["required_organ"] = filters["required_organ"]
        if filters.get("urgency"):
            conditions.append("urgency = %(urgency)s")
            values["urgency"] = filters["urgency"]
        if filters.get("blood_group"):
            conditions.append("blood_group = %(blood_group)s")
            values["blood_group"] = filters["blood_group"]

    where = "WHERE " + " AND ".join(conditions)
    rows = frappe.db.sql(
        f"""
        SELECT name, patient_name, required_organ, blood_group, urgency,
               hospital, waitlist_date, status
        FROM `tabRecipient`
        {where}
        ORDER BY
          CASE urgency WHEN 'Super Urgent' THEN 1 WHEN 'Urgent' THEN 2 ELSE 3 END,
          waitlist_date ASC
        """,
        values,
        as_dict=True,
    )
    for row in rows:
        if row.get("waitlist_date"):
            row["days_waiting"] = date_diff(today(), row["waitlist_date"])
    return rows


def get_chart(data):
    organ_counts = {}
    for row in data:
        organ_counts[row["required_organ"]] = organ_counts.get(row["required_organ"], 0) + 1
    return {
        "data": {
            "labels": list(organ_counts.keys()),
            "datasets": [{"values": list(organ_counts.values())}],
        },
        "type": "bar",
        "title": "Waiting List by Organ",
        "colors": ["#5e64ff"],
    }
