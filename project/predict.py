'''Predicts usesr based on tweets'''
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    '''
    Compares and returns which user is most likely to make given tweet
    '''
    # Get user from DB, user has to be in DB
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    # Grab tweet vector from each tweet for each user
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Vertically stack vects to get one array
    vects = np.vstack([user0_vects, user1_vects])
    labels = np.concatenate([np.zeros(len(user0.tweets)),
                            np.ones(len(user1.tweets))])

    # Fit model wiht x == vects and y == labels
    log_reg = LogisticRegression().fit(vects, labels)

    # Vectorize hypo tweet to pass in .predict()
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    return log_reg.predict(hypo_tweet_vect.reshape[1, -1])
