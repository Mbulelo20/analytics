from google.oauth2 import service_account
from googleapiclient.discovery import build

# Replace 'YOUR_SERVICE_ACCOUNT_JSON_FILE.json' with the path to your JSON service account file
credentials = service_account.Credentials.from_service_account_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
)

# Create the YouTube Analytics API service
youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
print("(****************************)")
response = youtube_analytics.reports().query(
    ids='channel==MINE',  # Replace with the appropriate channel or video ID
    startDate='2023-02-21',
    endDate='2023-02-23',
    metrics='views,likes,dislikes,shares',
    dimensions='video'
).execute()

print(response)