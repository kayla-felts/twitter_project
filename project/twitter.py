''' Get tweets and users from Twitter DB'''
from os import getenv
import tweepy
import spacy
from .models import DB, Tweet, User

# make suthenticator handler
TWITTER_AUTH = tweepy.OAuthHandler(
    getenv('TWITTER_API_KEY'),
    getenv('TWITTER_API_KEY_SECRET')
)

TWITTER = tweepy.API(TWITTER_AUTH)

# Load vect2vect model
nlp = spacy.load('my_model/')


def vectorize_tweet(tweet_text):
    '''
    turns tweet text into vectors
    '''
    return nlp(tweet_text).vector


def add_or_update_user(username):
    '''
    get users and tweets from twitter DB
    '''
    try:
        # gets back twitter object
        twitter_user = TWITTER.get_user(username)
        # updates or adds user to our DB
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)
        DB.session.add(db_user)

        # grabs tweets from 'twitter user'
        tweets = twitter_user.timeline(
            count=200,
            exlude_replies=True, 
            nclude_rts=False,
            tweet_mode='extended',
            since_id=db_user.newest_tweet_id
        )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            # typye(tweet) == object
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(
                id=tweet.id, text=tweet.full_text[:300], vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    # prints error message
    except Exception as e:
        print(f'Error Processing {username}: {e}')
        return e

    else:
        DB.session.commit()

