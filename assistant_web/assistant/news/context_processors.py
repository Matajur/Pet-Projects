import requests
from .views import fetch_news
from django.conf import settings


def news_widget(request):
    """
    The news_widget function is a view that returns the latest news items.

    :param request: Get the language from the session
    :return: A dictionary
    :doc-author: Trelent
    """
    lang = request.session.get(settings.LANGUAGE_SESSION_KEY, "en")
    latest_news = fetch_news(lang)
    return {"latest_news": latest_news}


def currency_data(request):
    """
    The currency_data function returns a dictionary of currency data.
    The keys are the currency codes, and the values are their exchange rates.

    :param request: Pass the request object to the view
    :return: A dictionary with two keys:
    :doc-author: Trelent
    """
    currency = ["USD", "EUR"]
    response_currency = requests.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    )
    data = response_currency.json()
    currency_info = {}
    for item in data:
        if item["cc"] in currency:
            currency_info[item["cc"]] = item["rate"]
    return {"currency_data": currency_info}
