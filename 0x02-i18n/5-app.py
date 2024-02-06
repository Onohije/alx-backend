#!/usr/bin/env python3
"""5. Mock logging in"""

from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """Configuration Class for Flask App"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """returns a user dictionary or None"""
    return users.get(int(request.args.get('login_as', None)))


@app.before_request
def before_request():
    """Uses get_user to find a user"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Get User locale from flask request"""
    locale = request.args.get('locale', None)
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Index page"""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run()
