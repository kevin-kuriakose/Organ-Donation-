
app_name = "organ_donation"
app_title = "Organ Donation Trust"
app_version = "2.0.0"

fixtures = ["Custom Field", "Property Setter", "Notification", "Workflow", "Web Form"]

doc_events = {
    "Donor": {
        "after_insert": "organ_donation.api.patient_sync.create_patient_from_donor"
    }
}
