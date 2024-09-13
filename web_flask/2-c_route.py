#!/usr/bin/python3
"""
   This module defines a script that starts a Flask web application.
"""
from flask import Flask, escape
app = Flask(__name__)


@app.route('/', strict_slashes=False)
# Route for the root path
def hello_hbnb():
    """
       Method print text
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
# Route for the /hbnb path
def hbnb():
    """
       Method print text
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
# Route for the /c/<text> path
def custom_text(text):
    """
       Method format text
    """
    # Replace underscore symbols with a space
    text = escape(text).replace('_', ' ')
    return 'C {}'.format(text)


if __name__ == '__main__':
    # Run the Flask app on 0.0.0.0, port 5000
    app.run(host='0.0.0.0', port=5000)
