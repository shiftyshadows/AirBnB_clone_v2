#!/usr/bin/python3
""" This module defines a script that starts a Flask web application."""
from flask import Flask, escape, render_template

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


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
# Route for the /python/<text> path with default value "is cool"
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    # Replace underscore symbols with a space
    text = escape(text).replace('_', ' ')
    return 'Python {}'.format(text)


@app.route('/number/<int:n>', strict_slashes=False)
# Route for the /number/<n> path
def show_number(n):
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
# Route for the /number_template/<n> path
def number_template(n):
    # Display an HTML page if n is an integer
    return render_template('number_template.html', number=n)


if __name__ == '__main__':
    # Run the Flask app on 0.0.0.0, port 5000
    app.run(host='0.0.0.0', port=5000)
