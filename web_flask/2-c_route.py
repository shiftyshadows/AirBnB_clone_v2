#!/usr/bin/python3
""" A module that starts a Flask web application. """
from flask import Flask, escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
# Route for the root path
def hello_hbnb():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
# Route for the /hbnb path
def hbnb():
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
# Route for the /c/<text> path
def custom_text(text):
    # Replace underscore symbols with a space
    text = escape(text).replace('_', ' ')
    return 'C {}'.format(text)


if __name__ == '__main__':
    # Run the Flask app on 0.0.0.0, port 5000
    app.run(host='0.0.0.0', port=5000)
