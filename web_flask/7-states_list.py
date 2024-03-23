#!/usr/bin/python3
'''
   A simple flask application.
'''
from flask import Flask, render_template
from models import storage

#Starts the application instance
app=Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_session(exception=None):
    """
       Method to remove SQLAlchemy session
       after each request.
    """
    storage.close()


@app.route('/states_list', methods=['GET'])
def states_list():
    """
       Display HTML page with list of states
    """
    all_states = list(storage.all("State").values())  # Fetch all State objects
    all_states.sort(key=lambda state: state.name)
    ctxt = {
        'states': all_states
    }

    return render_template('7-states_list.html', **ctxt)


@app.route('/')
def index():
    ''' Defines the index page. '''
    return 'Hello HBNB'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
