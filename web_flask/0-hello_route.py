#!/usr/bin/python3
""" This module defines a flask application."""
from flask import Flask

app = Flask(__name__)


# Route definition with strict_slashes=False
@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Default route for /"""
    return "Hello HBNB!"


if __name__ == '__main__':
    # Run the application on 0.0.0.0, port 5000
    app.run(host='0.0.0.0', port=5000)
