"""
    Run using: exec(open('pull-tweets.py').read())
    Analyse using: get_contexts('')

    TODO: Cache API keys after first run
    TODO: Build an interact REPL
    TODO: Color the word in the contexts and make it easier to navigate through (npyscreen)
    TODO: Cache results to file in order to lower Twitter API calls (rate limit)
"""

import os
import collections

import tweepy as tw

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

# Twitter API/Secret keys
consumer_key= ''
consumer_secret= ''
access_token= ''
access_token_secret= ''

class Context:
    """
    Used to stop yourself from coming to a conclusion based on single
    word. Rather, you can look at the different contexts that a person
    uses a word inside of to see what they really mean.
    """
    def __init__(self, word, context):
        # The word to provide context for
        self.word = word
        # Context is the tweet itself
        self.context = context

def get_contexts(word):
    """
    Returns a list of the tweets that the word was used inside of. 
    """
    c = []
    for ctx in contexts:
        if ctx.word == word:
            c.append(ctx.context)
    
    for r in c:
        print(r + '\n')

# Authenticate with Twitter
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Collect handle/username
username = input('Enter Twitter handle/username: ')

# Retrieve stop words (NLTK)
stop_words = set(stopwords.words('english')) 

# Context storage
contexts = []

print('[+] Collecting and analyzing tweets...')
counter = collections.Counter()
count = 0
for status in tw.Cursor(api.user_timeline, id=username, tweet_mode='extended', include_rts=False).items():
    # Retrieve the tweet
    tweet = status.full_text
    count = count + 1

    # Split the tweet up into separate words
    words = tweet.split()
    for word in words:
        # Filter stop words
        word = word.lower()
        if not word in stop_words:
            contexts.append(Context(word, tweet))
            counter.update({word: 1})
            
print('[+] Analyzed ({})\n[+] Results ->'.format(count))

# Save and print
mostcommon = counter.most_common(50)
print(mostcommon)