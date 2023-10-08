from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('analytics/youtube', views.youtube_analytics, name="youtube_analytics"),
    path('test', views.test, name="test")
]
