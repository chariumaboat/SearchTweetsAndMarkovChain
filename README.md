# SearchTweetsAndMarkovChain
Search for the phrase specified by the argument.
Reconstruct the searched sentences in a Markov chain.
And make useless tweets.

## How to deploy
- Installation of required libraries

```bash
pip install tweepy
pip install janome
pip install markovify
pip install python-dotenv
```

- API settings
```bash
touch .env
vi .env
```

```bash
consumer_key='$YourAPIKey'
consumer_secret='$YourAPIKey'
access_key='$YourAPIKey'
access_secret='$YourAPIKey'
```

- Run

```bash
python SearchTweetsAndMarkovChain.py -w '$SearchWord'
python SearchTweetsAndMarkovChain.py -w '$SearchWord1 $SearchWord2 $SearchWord3'
```
