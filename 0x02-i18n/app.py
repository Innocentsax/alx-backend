#!/usr/bin/env python3
"""A simple flask app
"""


from flask import Flask, render_template, request, g
from flask_babel import Babel
from pytz import timezone
import pytz.exceptions
from datetime import datetime
import locale


class Config(object):
	"""_summary_

	Returns:
					_type_: _description_
	"""
	LANGUAGES = ['en', 'fr']
	BABEL_DEFAULT_LOCALE = 'en'
	BABEL_DEFAULT_TIMEZONE = 'UTC'


# configure the flask app
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


users = {
	1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
	2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
	3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
	4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
	"""returns a user dictionary or None if the ID cannot be found
	"""
	login_id = request.args.get('login_as')
	if login_id:
		return users.get(int(login_id))
	return None


@app.before_request
def before_request() -> None:
	"""_summary_
	"""
	user = get_user()
	g.user = user
 
	time_now = pytz.utc.localize(datetime.utcnow())
	time = time_now.astimezone(timezone(get_timezone()))
	locale.setlocale(locale.LC_TIME, (get_locale(), 'UTF-8'))
	time_format = "%b %d, %Y %I:%M:%S %p"
	g.time = time.strftime(time_format)


@babel.localeselector
def get_locale():
	"""_summary_

	Returns:
					_type_: _description_
	"""
	# Locale from URL parameters
	locale = request.args.get('locale')
	if locale in app.config['LANGUAGES']:
		return locale

	# Locale from user settings
	if g.user:
		locale = g.user.get('locale')
		if locale and locale in app.config['LANGUAGES']:
			return locale

	# ocale from request header
	locale = request.headers.get('locale', None)
	if locale in app.config['LANGUAGES']:
		return locale

		# Default locale
	return request.accept_languages.best_match(app.config['LANGUAGES'])

# babel.init_app(app, locale_selector=get_locale)


@babel.timezoneselector
def get_timezone():
	"""
	Select and return appropriate timezone
	"""
	# Find timezone parameter in URL parameters
	tzone = request.args.get('timezone', None)
	if tzone:
		try:
			return timezone(tzone).zone
		except pytz.exceptions.UnknownTimeZoneError:
			pass

	# Find time zone from user settings
	if g.user:
		try:
			tzone = g.user.get('timezone')
			return timezone(tzone).zone
		except pytz.exceptions.UnknownTimeZoneError:
			pass

	# Default to UTC
	default_tz = app.config['BABEL_DEFAULT_TIMEZONE']
	return default_tz


@app.route('/')
def index():
	"""_summary_
	"""
	return render_template('5-index.html')


if __name__ == '__main__':
	app.run(port="5000", host="0.0.0.0", debug=True)
