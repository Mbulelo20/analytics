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

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    youtube_data = build('youtube', 'v3', credentials=creds)

    # Create the YouTube Analytics service
    youtube_analytics = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    return {"yt_analytics":youtube_analytics,"yt_data": youtube_data}

def get_channel_name(youtube_data):

    # Call the channels().list() method to retrieve channel information
    channels_response = youtube_data.channels().list(
        part='snippet',
        mine=True  # Retrieves the channel information for the authenticated user
    ).execute()

    # Extract the channel name from the response
    channel_name = channels_response['items'][0]['snippet']['title']

    return channel_name

def date_range(start, end):
    return start, end


# Fetch basic channel statistics
def get_channel_statistics(youtube_analytics, start, end, dimension):
    print(start)
    print(end)
    response = youtube_analytics.reports().query(
        ids='channel==MINE',
        startDate=start,
        endDate='2023-11-07',
        metrics='views,comments,likes,dislikes,shares,subscribersGained,subscribersLost',
        dimensions=dimension
    ).execute()

    return response


def get_all_videos_for_channel(youtube_data):
    videos = []
    next_page_token = None
    while True:
        # Use the search().list() method to fetch videos for a specific channel
        search_response = youtube_data.search().list(
            channelId='UC34feEA9roBAW9o1561szQw',
            # maxResults=50,  # You can adjust the number of results per page
            pageToken=next_page_token,
            type='video',
            part='id'
        ).execute()

        # Add the video IDs to the list
        for item in search_response.get('items', []):
            videos.append(item['id']['videoId'])

        # Check if there are more pages of results
        next_page_token = search_response.get('nextPageToken')

        if not next_page_token:
            break
    
    return videos

def youtubeData(start, end, dimension):
    
    youtube_service = get_authenticated_service()
    name = get_channel_name(youtube_service["yt_data"])
    stats = get_channel_statistics(youtube_service["yt_analytics"], start, end, dimension)
    videos = get_all_videos_for_channel(youtube_service["yt_data"])

    data = {
        "channel_name": name,
        "stats": stats,
        "videos": videos
    }

    file_path = "bulkdata.json"

    # Write the data to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

    return data

# def main():
#     print(youtubeData("2023-06-01","2023-09-01"))

# if __name__ == '__main__':
#     main()
