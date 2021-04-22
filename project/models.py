from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return f'User: {self.name}'


class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref(
        'tweets', lazy=True))

    def __repr__(self):
        return f'Tweet: {self.text}'


def insert_example_users():
    kayla = User(id=1, name='Kayla')
    jasmine = User(id=2, name='Jasmine')
    DB.session.add(kayla)
    DB.session.add(jasmine)
    DB.session.commit()
