import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

import json

# Your API credentials file (JSON) obtained from the Google Developer Console
CLIENT_SECRETS_FILE = 'client_secret.json'

# The YouTube Analytics and Reporting API version
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'

# The scope for the YouTube Data API (read-only)
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

global aa
aa = None
# Initialize the YouTube Analytics and Reporting service
def get_authenticated_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials, or if the credentials are expired, refresh them
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Create the YouTube Analytics service
    youtube_analytics = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
    aa = creds
    return youtube_analytics

def channel():
    return build('youtube', 'v3', credentials=aa)


# Fetch basic channel statistics
def get_channel_statistics(youtube_analytics):
    channels_response = channel().channels().list(
            part='snippet',
            id="UC34feEA9roBAW9o1561szQw"
        ).execute()
    channel_name = channels_response['items'][0]['snippet']['title']

    # Print the channel name
    print(f'Channel Name: {channel_name}')
    response = youtube_analytics.reports().query(
        ids='channel==MINE',
        startDate='2023-02-21',
        endDate='2023-02-23',
        metrics='views,comments,likes,dislikes,shares,subscribersGained,subscribersLost',
        dimensions='day'
    ).execute()

    return response

def main():
    youtube_analytics = get_authenticated_service()
    get_channel_statistics(youtube_analytics)

if __name__ == '__main__':
    main()
