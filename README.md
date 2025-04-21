# Salesforce Campaign Data Parser

A Python tool for parsing and cleaning campaign data exported from Salesforce. This script reads a CSV file containing **ACTIONCAMPAIGNID** and **CAMPAIGN_COOKIE_DATA_JSON** columns, decodes and parses the JSON in the `CAMPAIGN_COOKIE_DATA_JSON` field, cleans up UTM parameters, and generates a new CSV file with structured and cleaned data.

## Features

- Decodes and parses URL-encoded JSON data from Salesforce campaign tracking data.
- Cleans up UTM parameters, ensuring the values are readable and properly decoded.
- Handles missing or incomplete data, skipping rows and logging the issues.
- Outputs a clean, structured CSV with user-friendly column headers and progress updates.
- Uses a terminal progress bar to track processing status for large datasets.

## Prerequisites

Before you can run the script, ensure you have the following installed:

- Python 3.6 or higher
- Python libraries:
  - `tqdm` for the progress bar
  - `json`, `csv`, and `urllib.parse` (these are part of Python's standard library, so no installation needed)

You can install `tqdm` via pip:

```bash
pip install tqdm
