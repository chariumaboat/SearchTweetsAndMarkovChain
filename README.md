# SearchTweetsAndMarkovChain
Search for the phrase specified by the argument.
Reconstruct the searched sentences in a Markov chain.
And make useless tweets.

## How to deploy
- Installation of required libraries

```bash
pip install -r requirements.txt
```

- API settings
  - make `setting.ini`
  - [docs](https://docs.python.org/ja/3/library/configparser.html)

- Run

```bash
python SearchTweetsAndMarkovChain.py -w '$SearchWord' -e '$EnvName'
python SearchTweetsAndMarkovChain.py -w '$SearchWord1 $SearchWord2 $SearchWord3' -e '$EnvName'
```
