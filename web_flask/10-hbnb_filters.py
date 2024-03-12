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
    Teardown method to remove the current SQLAlchemy Session.
    """
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Display a HTML page with filters.
    """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    amenities = sorted(list(storage.all("Amenity").values()), key=lambda x: x.name)
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
