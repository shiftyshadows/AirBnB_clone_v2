#!/usr/bin/python3
""" This module defines a script that starts a Flask web application."""
from flask import Flask, escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ This route return a string. """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ This route return a string. """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def custom_text(text):
    """ This route return a custom string. """
    text = escape(text).replace('_', ' ')
    return 'C {}'.format(text)


if __name__ == '__main__':
    # Run the Flask app on 0.0.0.0, port 5000
    app.run(host='0.0.0.0', port=5000)
