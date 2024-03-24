import requests
import re
from bs4 import BeautifulSoup
import sys
from util import generate_text, wakati, auth_api_v2, reverse_retranslation
import re


def remove_urls(text):
    # URLの正規表現パターン
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    # URLを空文字列で置換
    cleaned_text = re.sub(url_pattern, '', text)
    return cleaned_text


def cleanhtml(raw_html):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def scraping(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, "lxml")
    text = soup.find_all("a", {"class", re.compile("skin-titleLink.*")})
    text = cleanhtml([i.text for i in text][0])
    return text


def main():
    f = open('./data/raw_omani_text', 'r', encoding='UTF-8')
    getTxt = f.read()
    f.close()
    try:
        getTxt = remove_urls(getTxt)
    except:
        pass
    tweet_text = generate_text(wakati(getTxt))
    try:
        tweet_text = reverse_retranslation(tweet_text)
    except:
        pass
    print(tweet_text)
    # trim
    tweet_text_140 = tweet_text[0:120]
    print("-----Post Text trimmed to 140 characters-----")
    print(len(tweet_text_140))
    print(tweet_text_140)
    # tweet
    api = auth_api_v2(sys.argv[1])
    try:
        post_tweet = api.create_tweet(text=tweet_text_140)
    except Exception as e:
        print(e)
    else:
        print("-----Post Tweet Response-----")
        print(post_tweet)


if __name__ == "__main__":
    main()
