#!/usr/bin/python3
"""
Script that starts a Flask web application.
"""

import logging
from flask import Flask, render_template
from models import storage

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.teardown_appcontext
def teardown_session(exception):
    """Closes the database session."""
    storage.close()

@app.errorhandler(Exception)
def handle_error(e):
    """Handles internal server errors."""
    logging.error("An error occurred: %s", str(e))
    return 'An internal server error occurred', 500

@app.route('/states', strict_slashes=False)
def states_list():
    """Displays a list of all State objects."""
    states = storage.all("State").values()
    states_sorted = sorted(states, key=lambda x: x.name)
    return render_template('9-states.html', states=states_sorted)

@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Displays cities of a specific State."""
    state = storage.get("State", id)
    if state is None:
        return render_template('9-states.html', not_found=True)
    cities_sorted = sorted(state.cities, key=lambda x: x.name)
    return render_template('9-states.html', state=state, cities=cities_sorted)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
