# PM_Budget_tracker

# Project Budget Tracker

A clean, form-based Streamlit application to track internal project costs against an approved client budget.

This tool is designed for project managers and operations teams who want accurate budget utilization tracking without using spreadsheet-style interfaces.

---

## Features

- Form-based data entry (Google Forms style)
- Track internal FL costs:
  - Translator fees
  - Checker fees
  - MTPE fees
  - FR fees
  - Formatting fees
  - LSO fees
  - LQA fees
- Supported calculation methods:
  - Per word
  - Per minute
  - Per hour
  - Per page
  - Per character
  - Flat fee
- Decimal-safe input for rates and volumes
- Delete individual cost entries
- Client-approved budget tracking
- Automatic budget utilization calculation
- Visual budget health indicators:
  - Green: under 80 percent
  - Yellow: 80 percent and above
  - Red: 100 percent and above
- CSV exports with correct accounting structure:
  - Line-level cost details
  - Project-level budget summary
- Simple, professional UI with clear visual hierarchy

---

## What This Tool Is (and Is Not)

### This tool IS
- A single-project budget tracker
- Focused on internal cost control
- Finance-safe and audit-friendly
- Easy to use for non-finance users

### This tool IS NOT
- An invoicing system
- A multi-project portfolio tracker
- A spreadsheet replacement
- A billing or FX conversion tool

---

## Installation

### Prerequisites
- Python 3.10 or newer

### Install dependencies

```bash
pip install -r requirements.txt


How to Use

Enter the Client Approved Budget at the top of the page.

Add internal costs using the Add Internal Cost form.

Review added costs in the Internal Cost Breakdown section.

Monitor budget usage in the Budget Health section.

Export:

Cost details as CSV

Budget summary as CSV

Export Structure
Cost Details CSV

Contains one row per internal cost item:

Cost Type

Vendor

Method

Volume

Rate

Currency

Internal Cost

Budget Summary CSV

Contains project-level values only:

Client Budget

Budget Currency

Total Internal Cost

Budget Utilization Percent

This separation prevents incorrect duplication of summary data.

Design Principles

Clear separation between line-level data and project-level metrics

No spreadsheet-style editing

Minimal dependencies

Predictable calculations

Clean and readable UI

Possible Future Enhancements

These are intentionally not included but can be added later:

Milestone-based budgets

Client-facing export (hide vendor and rates)

Edit modal for cost entries

Excel (.xlsx) export

Persistent storage (database)
