# Google Play Store Data Outlook Event Creation

This repository contains scripts to process Google Play Store data from Google Takeout and create Outlook calendar events using the Microsoft Graph API.

## Features
1. **Data Conversion**: Convert Google Play Store JSON files to CSV.
2. **Data Merging**: Combine multiple CSV files into a unified dataset.
3. **Event Creation**: Create Outlook calendar events for app/library entries.
4. **Logging**: Maintain logs for processed events and last event creation.

## Workflow Summary
1. Download your Google Play Store data from Google Takeout.
2. Preprocess the data by converting JSON files to CSV and merging them.
3. Use `create_events.py` to create Outlook events from the combined data.
4. Check logs for details and track processing.

## Prerequisites
- **Microsoft Graph API Credentials**: `client_id`, `tenant_id`, `client_secret`, `user_id`
- **Required Libraries**: `pandas`, `numpy`, `requests`, `pytz`

## Usage

### Step 1: Obtain Your Google Play Store Data
1. Go to [Google Takeout](https://takeout.google.com/).
2. Select **Google Play Store** as the data source.
3. Download the data as a ZIP file.
4. Extract the following files from the path:
   ```
   takeout-<timestamp>.zip\Takeout\Google Play Store\
   ```
   - `Library.json`
   - `Purchase History.json`

### Step 2: Convert JSON Files to CSV
1. Run `create_1_library_csv.py` to convert `Library.json` to `Library.csv`.
2. Run `create_2_purchase_history_csv.py` to convert `Purchase History.json` to `Purchase History.csv`.

### Step 3: Merge Data
1. Run `create_3_combine_library_purch_hist.py` to merge `Library.csv` and `Purchase History.csv` into a unified dataset `combine_library_purch_hist.csv`.

### Step 4: Create Outlook Calendar Events
1. Run `create_4_events.py` to process `combine_library_purch_hist.csv` and create Outlook calendar events using the Microsoft Graph API.

## Logs
Two logs are created for tracking progress:
1. **Create Events Log**: Tracks processing details and errors during event creation (`create_events_log.txt`).
2. **Last Event Log**: Tracks the most recent processed event to start from in future runs (`last_event_log.csv`).

## Example Directory Structure
```
repo/
|
├── create_1_library_csv.py
├── create_2_purchase_history_csv.py
├── create_3_combine_library_purch_hist.py
├── create_4_events.py
├── Library.json
├── Library.csv
├── Purchase History.json
├── Purchase History.csv
├── combine_library_purch_hist.csv
│── create_events_log.txt
│── last_event_log.csv
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.
