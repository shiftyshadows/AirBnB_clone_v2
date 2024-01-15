#!/usr/bin/python3
""" This module defines a script that starts a Flask web application."""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
# Method to handle teardown
def teardown(exception):
    storage.close()


@app.route('/states_list', strict_slashes=False)
# Route for /states_list
def states_list():
    # Get all State objects from storage and sort by name
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)

    # Render the HTML page
    return render_template('states_list.html', states=sorted_states)


if __name__ == '__main__':
    # Run the Flask app on 0.0.0.0, port 5000
    app.run(host='0.0.0.0', port=5000)
