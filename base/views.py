from django.shortcuts import render
from api import youtube

def home(request):
    # items = Item.objects.all()
    integration_list = [
        {"name": "youtube", "image": "/static/YouTube_icon_(2011-2013).svg.png"},
        {"name": "facebook", "image": "/static/fb.png"},
        {"name": "tiktok", "image": "/static/TikTok_Logo.jpg"}
    ]
    return render(request, 'home.html', {"integrations": integration_list})

def youtube_analytics(request):
    data = []
    youtube_service =youtube.get_authenticated_service()
 
    results = youtube.get_channel_statistics(youtube_service)

    print("Channel Statistics:")
    for row in results.get('rows', []):
        # playlist_starts = row[0]
        # playlist_saves_added = row[1]
        
        
        # data = {"playlist_starts": playlist_starts, "playlist_saves_added":playlist_saves_added}
        data.append(row)
        # print(f"Date: {date}, Views: {views}, Comments: {comments}, Likes: {likes}, Dislikes: {dislikes}, Shares: {shares}, Subscribers Gained: {subscribers_gained}, Subscribers Lost: {subscribers_lost}")
    context = {"data": data}
    
    return render(request, "analytics_page.html", context)


