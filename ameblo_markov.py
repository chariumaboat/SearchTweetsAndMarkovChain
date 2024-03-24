import requests
import re
from bs4 import BeautifulSoup
import sys
from util import generate_text, wakati, auth_api_v2, reverse_retranslation

# dragon-excalibur
# newhakogame1962
# ukannh


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
    blog_name = sys.argv[1]
    getTxt = ""
    for i in range(int(sys.argv[2])):
        url = f"https://ameblo.jp/{blog_name}/page-{i}.html"
        print(url)
        str_list = scraping(url)
        text = "".join(str_list)
        getTxt += text
    # Search for tweets data and generate text
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
    api = auth_api_v2(sys.argv[3])
    try:
        post_tweet = api.create_tweet(text=tweet_text_140)
    except Exception as e:
        print(e)
    else:
        print("-----Post Tweet Response-----")
        print(post_tweet)


if __name__ == "__main__":
    main()
