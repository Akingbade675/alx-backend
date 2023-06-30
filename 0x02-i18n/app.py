#!/usr/bin/env python3
'''Flask app'''


from flask import (Flask, render_template, request, g)
from flask_babel import (Babel, format_datetime)
from pytz import timezone
from datetime import datetime
import pytz.exceptions
import locale


app = Flask(__name__)
app.url_map.strict_slashes = False


class Config():
    '''Babel config class'''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    '''get logged in user'''
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request():
    '''use get_user to find a user if any,
    and set it as a global on flask.g.user
    '''
    g.user = get_user()

    time_now = pytz.utc.localize(datetime.utcnow())
    time = time_now.astimezone(timezone(get_timezone()))
    time_format = "%b %d, %Y %I:%M:%S %p"
    g.time = time.strftime(time_format)


@babel.localeselector
def get_locale():
    '''get best matched locale'''
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    if g.user:
        locale = g.user.get('locale')
        if locale in app.config['LANGUAGES']:
            return locale

    locale = request.headers.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    '''get timezone'''
    tzone = request.args.get('timezone')
    if tzone:
        try:
            return timezone(tzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user:
        try:
            tzone = g.user.get('timezone')
            return timezone(tzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    '''home page'''
    return render_template('index.html', date=format_datetime(datetime.now()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
