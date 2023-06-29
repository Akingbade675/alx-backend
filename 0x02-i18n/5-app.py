#!/usr/bin/env python3
'''Flask app'''


from flask import (Flask, render_template, request, g)
from flask_babel import Babel

app = Flask(__name__)


class Config():
    '''Babel config class'''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

babel = Babel(app)


def get_user():
    '''get logged in user'''
    users = {
        1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
        2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
        3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
        4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
    }

    login_id = int(request.args.get('login_as'))
    user = users.get(login_id)
    if user:
        return user
    return None


@app.before_request
def before_request():
    '''use get_user to find a user if any,
    and set it as a global on flask.g.user
    '''
    g.user = get_user()


@babel.localeselector
def get_locale():
    '''get best match locale'''
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    '''home page'''
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
