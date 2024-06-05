#!/usr/bin/python3
"""
   Script that starts a Flask web application.
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_session(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/cities_by_states', methods=['GET'])
def cities_by_states():
    """Display a HTML page with states and their cities"""
    all_states = list(storage.all("State").values())
    all_states.sort(key=lambda state: state.name)
    for state in all_states:
        state.cities.sort(key=lambda city: city.name)
    ctxt = {
        'states': all_states
    }
    return render_template('8-cities_by_states.html', **ctxt)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
