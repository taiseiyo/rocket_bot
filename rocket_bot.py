#!/usr/bin/env python3
import getpass
import urllib.request
from bs4 import BeautifulSoup
from rocketchat_API.rocketchat import RocketChat


user = getpass.getpass(prompt="User: ")
password = getpass.getpass()
rocket = RocketChat(user, password, server_url="***")


python_url = "https://qiita.com/tags/python"
javascript_url = "https://qiita.com/tags/javascript"


def get_html(url):
    req = urllib.request.Request(url)
    html = urllib.request.urlopen(req)
    html = html.read().decode("utf-8")
    return html


def get_url_info(html):
    message = ""
    target = BeautifulSoup(html, "lxml")
    trend_article = [tag.text for tag in target.find_all(
        "a", class_="css-eebxa eomqo7a4", href=True)]
    trend_url = [tag.get("href") for tag in target.find_all(
        "a", class_="css-eebxa eomqo7a4")]

    for info, url in zip(trend_article, trend_url):
        message = message + info + " " + url + "\n"
    return message


def get_messages(*htmls):

    messages = []
    for html in htmls:
        messages.append(get_url_info(html))
    return messages


def rocket_chat_tools(message):
    rocket.chat_post_message(
        message, channel="useful_programming_info").json()


def main():
    python_html = get_html(python_url)
    javascript_html = get_html(javascript_url)

    rocket.chat_post_message(""" Qiita 最新トレンド(先週 LGTM の多かっ
            た記事) 10 記事(Python 5 記事、JavaScript 5 記事)になりま
            す。今週も元気に一日頑張りましょう(^ ^)\n\n""",
                             channel="useful_programming_info").json()

    messages = get_messages(python_html, javascript_html)
    languages = ["Python 関連の記事", "JavaScript 関連の記事"]

    for message, language in zip(messages, languages):
        rocket_chat_tools(language+"\n"+message)


main()
