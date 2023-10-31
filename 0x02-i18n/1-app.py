#!/usr/bin/env python3
"""A simple flask app
"""


from flask import Flask, render_template
from flask_babel import Babel


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
babel = Babel(app)


@app.route('/')
def index():
    """_summary_
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
