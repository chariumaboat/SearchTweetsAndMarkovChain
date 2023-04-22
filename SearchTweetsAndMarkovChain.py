import sys
import random
import argparse
from janome.tokenizer import Tokenizer
import tweepy
from pprint import pprint
import configparser
from deep_translator import GoogleTranslator

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
if args.words == "" or args.env == "":
    print("No Argument")
    sys.exit()

# Split space separators into comma-separated lists
s = args.words
search_words = s.split()
print("search_words is " + str(search_words))

# select environment and Config
config = configparser.ConfigParser()
config.read('setting.ini')
envName = args.env
print("envName is " + envName)
consumer_key = config.get(envName, 'consumer_key')
consumer_secret = config.get(envName, 'consumer_secret')
access_key = config.get(envName, 'access_key')
access_secret = config.get(envName, 'access_secret')


def main():
    # Search for tweets data and generate text
    tweet_text = generate_text(wakati(tweet_search(search_words)))
    try:
        tweet_text = retranslation(tweet_text)
    except:
        pass
    print(tweet_text)
    # trim
    tweet_text_140 = tweet_text[0:139]
    print("-----Post Text trimmed to 140 characters-----")
    print(tweet_text_140)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    # tweet
    try:
        api.update_status(tweet_text_140)
    except Exception as e:
        print(e)
        print(type(e))

# Search 100 words passed from the argument


def tweet_search(search_words):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    set_count = 100
    word = search_words
    results = api.search(q=word, count=set_count)
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

# Create a dictionary by splitting text data using Janome


def wakati(text):
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    t = Tokenizer()
    result = t.tokenize(text, wakati=True)
    print("-----Generate words list-----")
    print(result)
    return result


def generate_text(words_list):
    num_sentence = 5
    words_list = words_list

    # Create a table for Markov chains
    markov = {}
    w1 = ""
    w2 = ""
    for word in words_list:
        if w1 and w2:
            if (w1, w2) not in markov:
                markov[(w1, w2)] = []
            markov[(w1, w2)].append(word)
        w1, w2 = w2, word
    # dict debug
    pprint(markov)
    # Automatic sentence generation
    count_kuten = 0  # "。"
    num_sentence = num_sentence
    sentence = ""
    w1, w2 = random.choice(list(markov.keys()))
    while count_kuten < num_sentence:
        try:
            tmp = random.choice(markov[(w1, w2)])
            # debug
            print("add text is " + tmp)
            sentence += tmp
        # I don't understand the meaning of this code
        except KeyError as e:
            print(e)
            break
        except Exception as e:
            print(e)
            print("type is " + type(e))
            break
        if (tmp == '。'):
            count_kuten += 1
            sentence += '\n'
        w1, w2 = w2, tmp

    print("-----Generated Text-----")
    print(sentence)

    return sentence


def retranslation(text):
    translated = GoogleTranslator(source='auto', target='en').translate(text)
    translated2 = GoogleTranslator(
        source='auto', target='ja').translate(translated)
    return translated2


if __name__ == "__main__":
    main()
