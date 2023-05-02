import sys
import random
import argparse
from janome.tokenizer import Tokenizer
import tweepy
from pprint import pprint
import configparser
from deep_translator import GoogleTranslator
from util import *

# Accepts search terms as arguments
search_words = []
parser = argparse.ArgumentParser(
    description='search words(space separated),environment name')
parser.add_argument('-w', '--words', metavar='words', type=str,
                    help='search words(space separated)', default="")
parser.add_argument('-e', '--env', metavar='env', type=str,
                    help='environment name', default="")
args = parser.parse_args()
print(args)
if args.env == "":
    print("No Argument")
    sys.exit()

envName = args.env

# Split space separators into comma-separated lists
s = args.words
search_words = s.split()
print("search_words is " + str(search_words))


def main():
    # Search for tweets data and generate text
    tweet_text = generate_text(wakati(tweet_search(search_words, envName)))
    try:
        tweet_text = retranslation(tweet_text)
    except:
        pass
    print(tweet_text)
    # trim
    tweet_text_140 = tweet_text[0:120]
    print("-----Post Text trimmed to 140 characters-----")
    print(len(tweet_text_140))
    print(tweet_text_140)
    # tweet
    api = auth_api_v2(envName)
    try:
        post_tweet = api.create_tweet(text=tweet_text_140)
    except Exception as e:
        print(e)
    else:
        print("-----Post Tweet Response-----")
        print(post_tweet)

def tweet_search(search_words, envName):
    # Search 100 words passed from the argument
    api = auth_api_v1(envName)
    # 特定ワードを検索する
    set_count = 100
    results = api.search_tweets(q=search_words, count=set_count)
    strResult = ""
    for result in results:
        # if "RT" not in result.text and "@" not in result.text:
        if "RT" not in result.text and "@" not in result.text and "https://t.co/" not in result.text:
            strResult += result.text
    print("-----Generate text based on this text-----")
    print(strResult)
    if strResult == "":
        sys.exit(0)
    print(strResult)
    return strResult




if __name__ == "__main__":
    main()
