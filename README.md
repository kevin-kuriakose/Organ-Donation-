# Organ Donation Trust – ERPNext v15+ Application

> Inspired by [Mohan Foundation](https://mohanfoundation.org) – India's leading organ donation NGO.  
> Built on **Frappe Framework v15+** and **ERPNext v15+**.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Application Architecture](#application-architecture)
4. [DocTypes](#doctypes)
5. [Reports](#reports)
6. [Workflows](#workflows)
7. [Notifications](#notifications)
8. [Web Forms (Portal)](#web-forms-portal)
9. [Scheduled Tasks](#scheduled-tasks)
10. [Roles & Permissions](#roles--permissions)
11. [Installation](#installation)
12. [Configuration](#configuration)
13. [ERPNext Healthcare Integration](#erpnext-healthcare-integration)
14. [Folder Structure](#folder-structure)
15. [Contributing](#contributing)

---

## Overview

The **Organ Donation Trust** app manages the end-to-end lifecycle of organ donation:

```
Donor Registration → Organ Pledge → Brain Death Certification
        → Family Consent → Organ Matching → Transplant Log
```

It integrates with ERPNext's Healthcare module (Patient, Medical Record) and provides a public-facing portal for donor and recipient self-registration.

---

## Features

| Feature | Description |
|---|---|
| Donor Management | Full donor profile with Aadhaar, blood group, status tracking |
| Organ Pledge | Submittable pledge with multi-organ child table |
| Brain Death Certificate | Dual-doctor certification with apnea test tracking |
| Family Consent | Organ-level consent with counseling notes |
| Organ Matching | Auto blood-group compatibility check, HLA score, workflow |
| Transplant Log | Surgical team, outcome, follow-up tracking |
| Hospital Registry | NOTTO registration, ROTTO zone, transplant centre flag |
| Reports | Donor Summary, Organ Match Report, Recipient Waiting List |
| Workflow | Organ Match Approval (Proposed → Review → Approved/Rejected) |
| Notifications | Email alerts for Brain Death, new Match, Transplant outcome |
| Scheduled Tasks | Daily digest, hourly super-urgent alert, pledge expiry |
| Portal | Public Web Forms for donor & recipient self-registration |
| ERPNext Integration | Auto-creates Patient from Donor, custom field on Patient |

---

## Application Architecture

```
organ_donation/
├── hooks.py                    ← App hooks, doc_events, scheduler
├── __init__.py                 ← Version
├── setup.py
├── requirements.txt
│
├── doctype/
│   ├── donor/
│   ├── recipient/
│   ├── organ_pledge/           ← includes child: Organ Pledge Detail
│   ├── brain_death_certificate/
│   ├── family_consent/         ← includes child: Family Consent Organ Detail
│   ├── hospital/
│   ├── organ_match/
│   └── transplant_log/
│
├── report/
│   ├── donor_summary/
│   ├── organ_match_report/
│   └── recipient_waiting_list/
│
├── workspace/
│   └── organ_donation/
│
├── notification/
│   ├── welcome_donor/
│   ├── brain_death_alert/
│   ├── organ_match_proposed/
│   └── transplant_success/
│
├── workflow/
│   └── organ_match_approval/
│
├── web_form/
│   ├── donor_registration/
│   └── recipient_registration/
│
├── api/
│   ├── matching.py             ← find_match(), auto_match() whitelist
│   ├── patient_sync.py         ← ERPNext Healthcare sync
│   ├── notifications.py        ← Programmatic email helpers
│   ├── queries.py              ← Whitelist search & dashboard stats
│   └── boot.py                 ← Boot session injection
│
├── tasks/
│   ├── daily.py
│   └── hourly.py
│
└── setup/
    └── install.py              ← Role & custom field creation on install
```

---

## DocTypes

### Donor
Primary record for every registered organ donor.

| Field | Type | Notes |
|---|---|---|
| donor_name | Data | Required |
| blood_group | Select | A+/A-/B+/B-/AB+/AB-/O+/O- |
| aadhaar | Password | Masked storage |
| status | Select | Registered → Pledged → Brain Dead → Consented → Organ Harvested |
| hospital | Link → Hospital | |
| donor_type | Select | Deceased / Living |

**Auto-creates** a Patient record in ERPNext Healthcare on insert.

---

### Recipient
Patient waiting for an organ transplant.

| Field | Type | Notes |
|---|---|---|
| patient_name | Data | Required |
| blood_group | Select | Required |
| required_organ | Select | Heart/Liver/Kidney/Lungs/Pancreas/Intestine/Cornea/Skin/Bone Marrow |
| urgency | Select | Routine / Urgent / Super Urgent |
| waitlist_date | Date | Auto-set to today on create |
| status | Select | Waiting → Matched → Transplanted |

---

### Organ Pledge *(Submittable)*
Formal pledge by the donor authorising organ donation.

- Child table `Organ Pledge Detail` for multiple organs
- Submission updates Donor status to **Pledged**
- Cancellation updates Donor status to **Withdrawn**

---

### Brain Death Certificate *(Submittable)*
Dual-doctor certification required under THO Act.

- Stores apnea test result, EEG flag
- Submission updates Donor status to **Brain Dead**
- Triggers `Brain Death Alert` email notification

---

### Family Consent *(Submittable)*
Records family member consent for each organ.

- Child table `Family Consent Organ Detail`
- Submission sets Donor to **Consented** or **Withdrawn**

---

### Organ Match *(Submittable)*
Links a Donor with a Recipient for a specific organ.

- Auto blood-group compatibility check on validate
- HLA match score field
- Subject to `Organ Match Approval` workflow
- Submission updates Donor → Organ Harvested, Recipient → Matched

---

### Transplant Log *(Submittable)*
Records the surgical procedure and outcome.

- Links to Organ Match
- Stores surgical team, duration, immunosuppression protocol
- Submission updates Recipient status to **Transplanted** or back to **Waiting**

---

### Hospital
Registry of hospitals and transplant centres.

- NOTTO registration number
- ROTTO zone (North/South/East/West/Central)
- Transplant centre flag

---

## Reports

### Donor Summary
Lists all donors with filters for status, blood group, state, and date range.

### Organ Match Report
Lists all organ matches with a donut chart breakdown by status.

### Recipient Waiting List
Prioritised waiting list (Super Urgent first, then by waitlist date) with days-waiting calculation and bar chart by organ.

---

## Workflows

### Organ Match Approval

```
[Proposed] ──── Send for Review ──▶ [Under Review]
                                         │
                              ┌──────────┴──────────┐
                          Approve                 Reject
                              │                     │
                        [Approved]            [Rejected]
                                                    │
                                               Reopen │
                                                    ▼
                                             [Proposed]
```

| State | Allowed Editor |
|---|---|
| Proposed | Transplant Coordinator |
| Under Review | Organ Donation Manager |
| Approved | — (submitted) |
| Rejected | — (cancelled) |

---

## Notifications

| Name | Trigger | Recipients |
|---|---|---|
| Welcome Donor | New Donor | Donor email |
| Brain Death Alert | Brain Death Certificate Submit | Transplant Coordinators + Managers |
| Organ Match Proposed | New Organ Match | Transplant Coordinators + Managers |
| Transplant Successful | Transplant Log Submit (outcome=Successful) | Transplant Coordinators + Managers |

---

## Web Forms (Portal)

| Form | Route | DocType |
|---|---|---|
| Donor Registration | `/donor-registration` | Donor |
| Recipient Registration | `/recipient-registration` | Recipient |

Both forms are accessible without login, allowing public registration.

---

## Scheduled Tasks

| Frequency | Task | Description |
|---|---|---|
| Daily | `send_waitlist_digest` | Email summary of waiting list to managers |
| Daily | `expire_old_pledges` | Mark pledges > 10 years as Expired |
| Hourly | `check_critical_recipients` | Alert coordinators of Super Urgent patients with no match |

---

## Roles & Permissions

| Role | Create | Read | Write | Submit | Delete |
|---|---|---|---|---|---|
| Organ Donation Manager | ✅ | ✅ | ✅ | ✅ | ✅ |
| Transplant Coordinator | ✅ | ✅ | ✅ | ✅ | ❌ |
| Hospital Admin | ❌ | ✅ | ❌ | ❌ | ❌ |

Roles are auto-created on `bench install-app organ_donation`.

---

## Installation

### Prerequisites

- Frappe Bench installed
- ERPNext v15+ installed and site created
- Python 3.10+, Node 18+

### Step 1 – Get the app

```bash
# From your bench directory
bench get-app organ_donation https://github.com/your-org/organ_donation.git

# OR for local development
bench get-app organ_donation /path/to/organ_donation
```

### Step 2 – Install on your site

```bash
bench --site your-site.localhost install-app organ_donation
```

### Step 3 – Run migrations

```bash
bench --site your-site.localhost migrate
```

### Step 4 – Build assets

```bash
bench build
bench --site your-site.localhost clear-cache
```

### Step 5 – Restart

```bash
bench restart
# or in development:
bench start
```

### Step 6 – Verify

1. Open your site in a browser
2. Navigate to **Organ Donation** workspace
3. Confirm DocTypes appear under the module

---

## Configuration

### Email Setup
Configure outgoing email in `Setup > Email Domain` for notifications to work.

### Healthcare Integration
If ERPNext Healthcare is installed, the app will automatically:
- Create a `Patient` record when a `Donor` is inserted
- Add a custom field `organ_donor_id` on the `Patient` DocType

If Healthcare is not installed, these steps are silently skipped.

### Export Fixtures
After customising notifications, workflows, or web forms in the UI:

```bash
bench --site your-site.localhost export-fixtures --app organ_donation
```

---

## ERPNext Healthcare Integration

The `patient_sync.py` module bridges Organ Donation with Healthcare:

```python
# Triggered via hooks.py doc_events
def create_patient_from_donor(doc, method):
    # Creates Patient with donor_name and blood_group
    # Runs only if tabPatient table exists
```

The `install.py` setup script adds `organ_donor_id` (Link → Donor) as a custom field on the `Patient` DocType.

---

## Folder Structure (Git-ready)

```
organ_donation/                 ← Git root
├── .gitignore
├── README.md
├── setup.py
├── requirements.txt
├── MANIFEST.in
└── organ_donation/             ← Python package
    ├── __init__.py
    ├── hooks.py
    ├── api/
    ├── doctype/
    ├── notification/
    ├── report/
    ├── setup/
    ├── tasks/
    ├── web_form/
    ├── workflow/
    └── workspace/
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and add tests
4. Run `bench --site your-site.localhost run-tests --app organ_donation`
5. Submit a pull request

---

## License

MIT License. See `LICENSE` file.

---

*Built with ❤️ in support of organ donation awareness in India.*
