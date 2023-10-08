from django.shortcuts import render
from api import youtube
import json
from django.http import JsonResponse

youtube_service = None
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
    results ={}
    modified_date_range = []
    date_range = ["Jan","Feb","March","April", "May", "Jun", "Jul","Aug","Sep","Oct","Nov","Dec"]

    youtube_service = youtube.get_authenticated_service()
    name = youtube.get_channel_name(youtube_service['yt_data'])
  
        
    results = youtube.get_channel_statistics(youtube_service, '2023-09-01', '2023-09-30')
    for row in results.get('rows', []):
        data.append(row)

    metrics = ["views","comments","likes","dislikes","shares","subscribersGained","subscribersLost" ]
    
    date_range_json = json.dumps(date_range)
    context = {"data": data,"channel_name":name, "metrics": metrics, "date_range":date_range_json}
    return render(request, "analytics_page.html", context)

def test(request):
    print("OK")
    youtube_service = youtube.get_authenticated_service()
    data=[]
    modified_date_range = []
    date_range = ["Jan","Feb","March","April", "May", "Jun", "Jul","Aug","Sep","Oct","Nov","Dec"]
    
    start = request.POST.get('start_date') #2023-09-01
    end = request.POST.get('end_date')

    first_month = start.split("-")[1] #09
    end_month = end.split("-")[1]
    if int(first_month)<10:
        first_month = [char for char in first_month][1]
    
    if int(end_month)<10:
        end_month = [char for char in end_month][1]
        
    name = youtube.get_channel_name(youtube_service['yt_data'])
    results = youtube.get_channel_statistics(youtube_service, '2023-09-01', '2023-09-30')
    for row in results.get('rows', []):
        data.append(row)
    date_range = date_range[int(first_month)-1:int(end_month)]
    date_range_json = json.dumps(date_range)

    metrics = ["views","comments","likes","dislikes","shares","subscribersGained","subscribersLost" ]
    
    date_range_json = json.dumps(date_range)
    context = {"data": data,"channel_name":name, "metrics": metrics, "date_range":date_range_json}

    return render(request, "analytics_page.html", context)

 

