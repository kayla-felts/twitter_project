'''Creating app file'''

from os import getenv
from flask import Flask, render_template, request
from .predict import predict_user
from .models import DB, User, Tweet
from .twitter import add_or_update_user


def create_app():
    '''
    Main function to bring project app together
    '''
    app = Flask(__name__)

    # Configure SQLAlchemy database
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    # Home endpoint route
    @app.route('/')
    def root():
        return render_template('base.html', title='Home',
                               users=User.query.all())

    # Update endpoint route
    @app.route('/update')
    def update():
        # Should update all current useres in DB
        # Should utalize add_or_update_user function
        return 'User Updated!'

    # Reset endpoint route
    @app.route('/reset')
    def reset():
        # Resets our DB
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset',
                               users=User.query.all())

    @app.route('/user', methods=["POST"])
    @app.route('/user/<name>', methods=["GET"])
    def user(name=None, message=''):

        # Take name passed in or pull it from request.values
        # to be accessed through user submission
        name = name or request.values['user_name']
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = f'User {name} Succesfully added!'

            tweets = User.query.filter(User.name == name).one().tweets

        # Error message
        except Exception as e:
            message = f'Error adding {name}: {e}'

            tweets = []

        return render_template('user.html', title=name, tweets=tweets,
                               message=message)

    # compare endpoint route
    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare users to themselves!'

        else:
            # prediction returns a 0 or 1
            prediction = predict_user(
                user0, user1, request.values['tweet_text'])
            message = "'{}' is more likely to be said by {} than {}!".format(
                request.values['tweet_text'],
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html', title='Prediction',
                               message=message)
    return app
