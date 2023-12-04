from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.news_list, name="root"),
    path("index/", views.main, name="index"),
    path("news/", views.news_list, name="news_list"),
    path("news_ua/<str:topic>/", views.news_list_ua, name="news_ua_topic"),
    path("news/<str:category>/", views.news_list, name="news_list_category"),
]
