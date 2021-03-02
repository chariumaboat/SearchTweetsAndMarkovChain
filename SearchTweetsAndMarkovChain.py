import sys
import random
import os
from dotenv import load_dotenv
import argparse
from janome.tokenizer import Tokenizer
import tweepy
from pprint import pprint


load_dotenv('.env') 

consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_key = os.environ.get('access_key')
access_secret = os.environ.get('access_secret')

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
    return strResult

# Create a dictionary by splitting text data using Janome
def wakati(text):
   text = text.replace('\n','')
   text = text.replace('\r','')
   t = Tokenizer()
   result =t.tokenize(text, wakati=True)
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
   count_kuten = 0 #  "。"
   num_sentence = num_sentence
   sentence = ""
   w1, w2  = random.choice(list(markov.keys()))
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
       if(tmp=='。'):
           count_kuten += 1
           sentence += '\n'
       w1, w2 = w2, tmp

   print("-----Generated Text-----")
   print(sentence)

   return sentence
    
if __name__ == "__main__":
    # Accepts search terms as arguments
    search_words = []
    parser = argparse.ArgumentParser(description='search words(space separated)')
    parser.add_argument('-w','--words',metavar='words',type=str,help='search words(space separated)',default="")
    args = parser.parse_args()
    print(args)
    if args.words == "":
        print("No Argument")
        sys.exit()
    # Split space separators into comma-separated lists
    s = args.words
    search_words = s.split()
    print(search_words)
    # Search for tweets data and generate text
    tweet_text = generate_text(wakati(tweet_search(search_words)))
    # trim
    tweet_text_140 = tweet_text[1:140]
    print("-----Text trimmed to 140 characters-----")
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