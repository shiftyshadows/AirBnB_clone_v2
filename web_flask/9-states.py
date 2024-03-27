#!/usr/bin/python3
""" A simple flask application. """
from models import storage
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_session(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/states')
@app.route('/states/<state_id>')
def states(state_id=None):
    """
       Display a HTML page with cities of a state
    """
    states_dict = list(storage.all('State').keys())
    instance_ids = []
    for state_item in states_dict:
        class_name, name_00, instance_id = state_item.split('.')
        instance_ids.append(instance_id)
    if state_id is None:
        all_states = list(storage.all("State").values())
        all_states.sort(key=lambda state: state.name)
        ctxt = {
            'states': all_states
        }
        return render_template('9-states.html', **ctxt)
    else:
        if state_id not in instance_ids:
            return render_template('not_found.html')
        else:
            states_objs = list(storage.all('State').values())
            for obj in states_objs:
                if state_id == obj.id:
                    state_cities = obj.cities
                    state_cities.sort(key=lambda city: city.name)
                    ctxt = {
                        'state': obj.name,
                        'cities': state_cities
                    }
                    return render_template('9-states.html', **ctxt)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
