from datetime import datetime
from django.shortcuts import render
import requests
from django.conf import settings
import json
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import News
from .scrap_news import articles_scraped
import time


def main(request):
    """
    The main function is the entry point for the news app.
    It renders a template called index.html, which displays all of the articles in our database.

    :param request: Get the request object that is sent to the view
    :return: The template index
    :doc-author: Trelent
    """
    return render(request, "news/index.html", {})


CATEGORIES = [
    ("main", "Головні"),
    ("war", "Війна"),
    ("world", "Світові"),
    ("society", "України"),
    ("economics", "Економіка"),
    ("science", "Наука"),
    ("sport", "Спорт"),
]

NEWSAPI_CATEGORIES = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology",
]


def parse_date(iso_date):
    """
    The parse_date function takes a string in ISO 8601 format and returns a datetime object.

    :param iso_date: Pass the date string to the function
    :return: A datetime object
    :doc-author: Trelent
    """
    return datetime.fromisoformat(iso_date.replace("Z", "+00:00"))


def get_news(category="general"):
    """
    The get_news function takes in a category as an argument and returns the top headlines from that category.
    The default value for the category is &quot;general&quot;.

    :param category: Specify the category of news you want to get
    :return: A list of dictionaries
    :doc-author: Trelent
    """
    url = "https://newsapi.org/v2/top-headlines"
    parameters = {
        "country": "us",
        "category": category,
        "apiKey": settings.NEWSAPI_KEY,
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    return data["articles"]


def news_list(request, category="general"):
    """
    The news_list function is responsible for rendering the news_list.html template,
    which displays a list of news articles from the News API. The function takes in an optional
    category parameter which specifies what category of news to display (e.g., business, entertainment).
    If no category is specified, then it defaults to &quot;general&quot;.

    :param request: Pass the request object to the view
    :param category: Filter the news by category
    :return: A rendered template
    :doc-author: Trelent
    """
    lang = request.session.get(settings.LANGUAGE_SESSION_KEY, "en")
    if lang == "uk":
        return HttpResponseRedirect(
            reverse("news:news_ua_topic", args=("main",)) + "?lang=uk"
        )

    news_data = get_news(category)
    for item in news_data:
        item["publishedAt"] = parse_date(item["publishedAt"]).strftime(
            "%d %B, %Y %H:%M"
        )
    context = {
        "news": news_data,
        "categories": NEWSAPI_CATEGORIES,
        "current_category": category,
    }
    return render(request, "news/news_list.html", context)


def news_list_ua(request, topic="main"):
    """
    The news_list_ua function is a view that displays the news in Ukrainian.
    It takes one argument, request, and returns an HttpResponseRedirect object if the language of the session is English.
    Otherwise it opens data.json file with UTF-8 encoding and loads its content into list_news variable as a dictionary object.
    Then it creates context dictionary with three keys: 'news', 'categories' and 'topic'. The value of each key depends on its name:
    the value for key &quot;news&quot; is equal to list_news[topic], where topic = &quot;main&quot; by default;
    the value for

    :param request: Get the request object
    :param topic: Select news from a specific category
    :return: The news_ua
    :doc-author: Trelent
    """
    lang = request.session.get(settings.LANGUAGE_SESSION_KEY, "en")
    if lang == "en":
        return HttpResponseRedirect(reverse("news:news_list") + "?lang=en")   
    
    news_data = News.objects.filter(topic=topic)
    
    # If there are no news for the selected topic in the database, scrape them
    if not news_data.exists():
        fill_news()
        news_data = News.objects.filter(topic=topic)
  
    context = {"news": news_data, "categories": CATEGORIES, "topic": topic}
    
    return render(request, "news/news_ua.html", context)


def fetch_news(lang="en"):
    """
    The fetch_news function fetches the latest news from the NewsAPI.
        Args:
            lang (str): The language of the news to be fetched. Defaults to English ('en').
        Returns:
            list[dict]: A list of dictionaries containing information about each article, including title, description and url.

    :param lang: Specify the language of news
    :return: A list of dictionaries
    :doc-author: Trelent
    """
    if lang == "en":
        url = (
            "https://newsapi.org/v2/top-headlines?country=us&apiKey="
            + settings.NEWSAPI_KEY
        )
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("articles", [])[:5]  # Limit news quantity to 5
        return []
    else:  # Ukrainian
        list_news = News.objects.filter(topic="main")
        # Return only 5 Ukrainian main news from database, you can adapt this part if necessary
        return list_news[:5]
    

def fill_news():  
    """
    The fill_news function allows users to create news and save them to the database.
    
    :doc-author: Trelent
    """
    news_data = articles_scraped()
    # with open("./data.json", "r", encoding="utf-8") as fl:
    #     news_data = json.load(fl)
    for key, value in news_data.items():        
        for el in value:
            News.objects.update_or_create(
                title = el['title'],
                content =el['content'],
                url = el['url'],
                date = el['date'],
                topic = key
                )    


    
