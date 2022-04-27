# Import  Python dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask dependency
from flask import Flask, jsonify

# Set up database engine
# The create_engine function allows us to access and query our SQLite 
# datebase file
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect our table
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link
session = Session(engine)

# Set up Flask

# Use magic method __name__ to check file source of running code
import app
print("example __name__ = %s", __name__)

if __name__ == "__main__":
    print("example is being run directly.")
else:
    print("example is being imported")

# Define the Flask app
app = Flask(__name__)

#--------------------
# Define route
#--------------------

@app.route("/")

# Create a function
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! \n
    Available Routes: \n
    /api/v1.0/precipitation 
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end    
    ''')

#----------------------
# Preciptitation Route
#----------------------

# Define preciptitation route
@app.route("/api/v1.0/precipitation")

# Create a function
def precipitation():
    # Calculate date for the previous year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query: Get the date and precipitation for the previous year.
    precipitation = session.query(Measurement.date,Measurement.prcp) .\
        filter(Measurement.date >= prev_year).all()

    # Create dictionary w/ jsonify    
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#----------------
# Station Route
#----------------

@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#---------------------------
# Monthly Temperature Route
#---------------------------

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))    
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    # Query to select the minimum, average, and maximum temps from our SQLite database.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps) 