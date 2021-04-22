'''Creating app file'''

from os import getenv
from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import update_all_users, add_or_update_user


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title='Home',
                               users=User.query.all())

    @app.route('/update')
    def update():
        update_all_users()
        return render_template('base.html', title='Useres Updated',
                               users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        add_or_update_user('jimmyfallon')
        add_or_update_user('genesimmons')
        return render_template('base.html', title='Reset',
                               users=User.query.all())

    return app
