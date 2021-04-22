'''SQLAlchemy User and Tweet models for DB'''
from flask_sqlalchemy import SQLAlchemy

# create DB from SQLAlchemy
DB = SQLAlchemy()


# Make User table
class User(DB.Model):
    '''
    Creates User Table
    '''
    # Make id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # Make nname column
    name = DB.Column(DB.String, nullable=False)
    # make newest tweet column
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f'User: {self.name}'


class Tweet(DB.Model):
    '''
    Track Tweets from each User
    '''
    # make id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # make text column
    text = DB.Column(DB.Unicode(300))
    # make vector column
    vect = DB.Column(DB.PickleType, nullable=False)
    # make user id column
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    # make user column
    user = DB.relationship('User', backref=DB.backref(
        'tweets', lazy=True))

    def __repr__(self):
        return f'Tweet: {self.text}'


# def insert_example_users():
#     kayla = User(id=1, name='Kayla')
#     jasmine = User(id=2, name='Jasmine')
#     DB.session.add(kayla)
#     DB.session.add(jasmine)
#     DB.session.commit()

CREATE_USER_TABLE_SQL = '''
    CREATE TABLE IF NOT EXIST user (
        id INT PRIMARY,
        name STRING NOT NULL
    );
    '''
