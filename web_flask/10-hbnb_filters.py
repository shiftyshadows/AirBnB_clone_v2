#!/usr/bin/python3
""" A simple flask application."""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_session(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/hbnb_filters')
def hbnb_filters():
    """
       Display a HTML page like 6-index.html with data
       from database.
    """
    all_states = list(storage.all("State").values())
    all_states.sort(key=lambda state: state.name)
    all_amenities = list(storage.all("Amenity").values())
    all_amenities.sort(key=lambda amenity: amenity.name)
    ctxt = {
        'states': all_states,
        'amenities': all_amenities
    }
    return render_template('10-hbnb_filters.html', **ctxt)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
