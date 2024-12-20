import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
from dateutil import parser
import sys 
import os


#--- Get msgraph config variables ---#
config_msgraph_path = os.getenv("ENV_VARS_PATH")  # Get path to directory contaiining config_msgraph.py
if not config_msgraph_path:
    raise ValueError("ENV_VARS_PATH environment variable not set")
sys.path.insert(0, config_msgraph_path)

from config_msgraph import config_msgraph

client_id=config_msgraph["client_id"]
tenant_id=config_msgraph["tenant_id"]
client_secret=config_msgraph["client_secret"]
user_id=config_msgraph["user_id"]

input_file = "combine_library_purch_hist.csv"

#--- Function to obtain an access token ---#
def get_access_token(client_id, tenant_id, client_secret):
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'client_id': client_id,
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raises an exception for HTTP error codes
    return response.json().get('access_token')

#--- Function to convert timezone and calculate end time  ---#
def append_duration_and_convert_time(df):
    est_zone = pytz.timezone('America/New_York')
    utc_zone = pytz.utc
    durations = []  # To store duration for each row
    start_times = []  # To store converted start times for each row
    end_times = []  # To store calculated end times for each row

    for _, row in df.iterrows():
        # Convert time to datetime object and adjust timezone
        start_time_utc = parser.parse(row['time']).replace(tzinfo=utc_zone)
        start_time_est = start_time_utc.astimezone(est_zone)
        start_times.append(start_time_est.strftime('%Y-%m-%dT%H:%M:%S'))
        
        # Calculate duration and end time
        if row['documentType'] == 'Tv Episode':
            duration = 50  # minutes
        elif row['documentType'] == 'Movie':
            duration = 100  # minutes
        else:
            duration = 0
        durations.append(duration)  # Append calculated duration
        end_time_est = start_time_est + timedelta(minutes=duration)
        end_times.append(end_time_est.strftime('%Y-%m-%dT%H:%M:%S'))
    
    # Add new columns to DataFrame
    df['start_time_est'] = start_times
    df['end_time_est'] = end_times
    df['duration'] = durations

#--- Function to create a calendar event using Microsoft Graph API ---#
def create_calendar_event(access_token, row):
    # Use the pre-calculated and formatted values directly
    start_time_formatted = row['start_time_est']
    end_time_formatted = row['end_time_est']
    duration_minutes = row['duration']  # Assuming duration is calculated in minutes in the DataFrame

    # create the event description, incorporating the duration
    description_html = (
        f"Title: {row['title']}<br>"
        f"Start: {start_time_formatted}<br>"
        f"End: {end_time_formatted}<br>"
        f"Duration: {duration_minutes} minutes<br>"
        f"Attributes: {(str(row['documentType']).replace(',', ', ') if pd.notna(row['documentType']) else 'None')}"
    )

    # Adjusted event payload to use the pre-calculated times and duration
    event_payload = {
        "subject": f"Google TV: {row['title']}",
        "start": {"dateTime": start_time_formatted, "timeZone": "America/Toronto"},
        "end": {"dateTime": end_time_formatted, "timeZone": "America/Toronto"},
        "body": {"contentType": "HTML", "content": description_html},
        "categories": ["Google TV"]
    }

    # Send the request to create the event
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    response = requests.post(f"https://graph.microsoft.com/v1.0/users/{user_id}/events", headers=headers, json=event_payload)
    response.raise_for_status()  # Ensure successful request


#--- Main script to process the CSV data and create events ---#
def main():
    access_token = get_access_token(client_id, tenant_id, client_secret)
    df = pd.read_csv(input_file) 
    df = df.dropna(subset=['time'])
    append_duration_and_convert_time(df)  # Convert times and append duration

    # Now iterate with the updated DataFrame including duration
    for index, row in df.iterrows():
        try:
            create_calendar_event(access_token, row)  # Ensure this function uses updated DataFrame columns
            # Success message adjustment to include the title from the DataFrame
            print(f"Event created for {row['start_time_est']} {row['title']}")
            #break
        except Exception as e:
            print(f"Failed to create event for {row['start_time_est']} {row['title']} Error: {e}")

if __name__ == "__main__":
    main()

