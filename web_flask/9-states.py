#!/usr/bin/python3
"""
Script that starts a Flask web application.
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Remove the current SQLAlchemy Session
    """
    storage.close()


@app.route('/states', strict_slashes=False)
def states_list():
    """
    Display a HTML page with a list of all State objects present in DBStorage sorted by name (A->Z)
    """
    states = storage.all("State").values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def states_cities(id):
    """
    Display a HTML page with the list of City objects linked to the State sorted by name (A->Z)
    """
    state = storage.get("State", id)
    if state:
        cities = sorted(state.cities, key=lambda city: city.name)
        return render_template('9-states.html', state=state, cities=cities)
    return render_template('9-states.html', not_found=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
