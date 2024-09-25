#!/usr/bin/python3
"""
This module defines a script that starts a Flask web application.

The web application listens on 0.0.0.0, port 5000, and has the following
routes:

1. `/`: Displays the message 'Hello HBNB!'.
2. `/hbnb`: Displays the message 'HBNB'.
3. `/c/<text>`: Displays 'C' followed by the value of the text variable.
    - The text variable replaces underscores with spaces in the output.
    - Example: `/c/hello_hbnb` returns `C hello hbnb`.

This module uses the `escape` function from Flask to ensure that the input
text is safely handled.
"""

from flask import Flask, escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    This route returns the string 'Hello HBNB!'.

    Returns:
        str: A string 'Hello HBNB!'.
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    This route returns the string 'HBNB'.

    Returns:
        str: A string 'HBNB'.
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def custom_text(text):
    """
    This route returns 'C' followed by the value of the `text` variable,
    with underscores replaced by spaces.

    Args:
        text (str): The input text from the URL, with underscores replaced
        by spaces.

    Returns:
        str: A formatted string 'C <text>'.
    """
    text = escape(text).replace('_', ' ')
    return 'C {}'.format(text)


if __name__ == '__main__':
    # Run the Flask app on 0.0.0.0, port 5000
    app.run(host='0.0.0.0', port=5000)
