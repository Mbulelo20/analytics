import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Your API credentials file (JSON) obtained from the Google Developer Console
CLIENT_SECRETS_FILE = 'client_secret.json'

# The YouTube Analytics and Reporting API version
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'

# The scope for the YouTube Data API (read-only)
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Initialize the YouTube Analytics and Reporting service
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube_analytics = build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)
    return youtube_analytics


# Fetch basic channel statistics
def get_channel_statistics(youtube_analytics):
    response = youtube_analytics.reports().query(
        ids='channel==MINE',
        startDate='2023-01-01',
        endDate='2023-10-05',
        metrics='views,comments,likes,dislikes,shares,subscribersGained,subscribersLost',
        dimensions='day'
    ).execute()

    print("Channel Statistics:")
    for row in response.get('rows', []):
        date = row[0]
        views = row[1]
        comments = row[2]
        likes = row[3]
        dislikes = row[4]
        shares = row[5]
        subscribers_gained = row[6]
        subscribers_lost = row[7]

        print(f"Date: {date}, Views: {views}, Comments: {comments}, Likes: {likes}, Dislikes: {dislikes}, Shares: {shares}, Subscribers Gained: {subscribers_gained}, Subscribers Lost: {subscribers_lost}")


def main():
    youtube_analytics = get_authenticated_service()
    get_channel_statistics(youtube_analytics)

if __name__ == '__main__':
    main()
