#!/usr/bin/python3
"""Script that starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
import os

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """After each request, remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display a HTML page with the list of states"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)
    return render_template('7-states_list.html', states=sorted_states)


if __name__ == '__main__':
    # Import SQL file into the database
    sql_file_path = os.path.join(os.path.dirname(__file__), 'main_0.sql')
    import_command = f"cat {sql_file_path} | mysql -hlocalhost -uroot -proot > /dev/null 2>&1"
    os.system(import_command)

    # Start Flask application
    app.run(host='0.0.0.0', port=5000)
