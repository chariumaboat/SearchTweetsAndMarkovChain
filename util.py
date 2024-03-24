import sys
import random
import argparse
from janome.tokenizer import Tokenizer
import tweepy
from pprint import pprint
import configparser
from deep_translator import GoogleTranslator


def auth_api_v2(envName):
    config = configparser.ConfigParser(interpolation=None)
    config.read('setting.ini')
    consumer_key = config.get(envName, 'consumer_key')
    consumer_secret = config.get(envName, 'consumer_secret')
    access_key = config.get(envName, 'access_key')
    access_secret = config.get(envName, 'access_secret')
    bearer_token = config.get(envName, 'bearer_token')
    client = tweepy.Client(bearer_token=bearer_token,
                           consumer_key=consumer_key,
                           consumer_secret=consumer_secret,
                           access_token=access_key,
                           access_token_secret=access_secret)
    return client


def auth_api_v1(envName):
    config = configparser.ConfigParser()
    config.read('setting.ini')
    consumer_key = config.get(envName, 'consumer_key')
    consumer_secret = config.get(envName, 'consumer_secret')
    access_key = config.get(envName, 'access_key')
    access_secret = config.get(envName, 'access_secret')
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api


def wakati(text):
    # Create a dictionary by splitting text data using Janome
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    t = Tokenizer()
    result = t.tokenize(text, wakati=True)
    print("-----Generate words list-----")
    print(result)
    return result


def generate_text(words_list):
    num_sentence = 5
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


def reverse_retranslation(text):
    text = text[::-1]
    translated = GoogleTranslator(source='auto', target='en').translate(text)
    translated2 = GoogleTranslator(
        source='auto', target='ja').translate(translated)
    return translated2
