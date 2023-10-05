from django.shortcuts import render

def home(request):
    # items = Item.objects.all()
    integration_list = [
        {"name": "youtube", "image": "/static/YouTube_icon_(2011-2013).svg.png"},
        {"name": "facebook", "image": "/static/fb.png"},
        {"name": "tiktok", "image": "/static/TikTok_Logo.jpg"}
    ]
    return render(request, 'home.html', {"integrations": integration_list})
