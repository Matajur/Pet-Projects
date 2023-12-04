import requests
from bs4 import BeautifulSoup
import time
import json
import os


def scrap_article(url: str):
    """
    The scrap_article function takes a url as an argument and returns a dictionary with the following keys:
        - content: The text of the article.
        - date: The date on which the article was published.


    :param url: str: Specify the type of data that will be passed to the function
    :return: A dictionary with two keys:
    :doc-author: Trelent
    """
    article_scrap = {}
    article_text = ""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    if response.status_code == 200:
        try:
            # time.sleep(1)
            date_published = soup.find(
                "div", attrs={"class": "article__info-item time"}
            ).text
            # date_published = time_published.split(' ')[1]
            # time.sleep(1)
            text_article = soup.find_all("div", attrs={"class": "article"})
            for n in text_article:
                article = reversed(n.find_all("p"))
                for el in article:
                    article_text += el.text
            article_scrap = {"content": article_text, "date": date_published}
        except:
            pass
    return article_scrap


def parse_news_ua(url: str, attr: str, limit=5):
    """
    The parse_news_ua function takes in a url and an attribute, and returns a list of dictionaries.
    The function scrapes the news website for the top 5 articles on that page,
    and then uses another function to scrape each article's content.
    It then creates a dictionary with all of this information, which is appended to the list.

    :param url: str: Pass the url of the news site
    :param attr: str: Specify the class of the news articles
    :param limit: Limit the number of news articles that are scraped
    :return: A list of dictionaries
    :doc-author: Trelent
    """
    list_news = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    if response.status_code == 200:
        # time.sleep(1)
        all_news = soup.find_all("a", attrs={"class": attr}, limit=limit)
        # time.sleep(1)
        for n in all_news:
            title_news = f"{n.find('img')['alt']}"
            url_news = n["href"]
            try:
                article = scrap_article(url_news)
                description = article["content"]
                date = article["date"]
                news_dict = {
                    "title": title_news,
                    "content": description,
                    "date": date,
                    "url": url_news,
                }
                list_news.append(news_dict)
            except:
                pass
    return list_news


def articles_scraped():
    """
    The articles_scraped function scrapes the news from unian.ua and saves it to a json file
    :return: A dictionary with the following structure:
    :doc-author: Trelent
    """
    all_data = {}
    list_topic_news = ["", "war", "science", "world", "society", "economics", "sport"]
    class1_topics = ["economics", "sport"]
    class2_topics = ["war", "science", "world", "society"]
    for topic in list_topic_news:
        if topic in class1_topics:
            attr_a = "list-news__image"
        elif topic in class2_topics:
            attr_a = "list-thumbs__image"
        else:
            attr_a = "list-news__image psr"

        url = "https://www.unian.ua/" + topic
        if topic == "":
            topic = "main"
        elif topic == "sport":
            url = "https://sport.unian.ua/"
        # Save data to the dictionary
        all_data[topic] = parse_news_ua(url, attr_a)
    # Write the data to the file after the loop
    # with open(
    #     os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data.json"),
    #     "w",
    #     encoding="utf-8",
    # ) as f:
    #     json.dump(all_data, f, ensure_ascii=False)
    return all_data

if __name__ == "__main__":
    articles_scraped()
