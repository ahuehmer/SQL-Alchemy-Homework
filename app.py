import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

###########################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

###########################
# Flask Setup
app = Flask(__name__)

###########################
# Flask Routes

@app.route("/")
def welcome():
    return (
        f"Welcome to Hawaii Weather App<br/><br/>"
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/><br/>"
        f" Please enter start and end dates in a yyyy-mm-dd format"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query recent precipitation data
    recent_date = dt.date(2017, 8 , 23)
    year_ago = recent_date - dt.timedelta(days=365)
    date_prcp = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    
    #Close session
    session.close()

    # Create a dictionary 
    precipitation = []
    for date, prcp in date_prcp:
        precipitation_dict = {date: prcp}
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query station data
    station_data = session.query(station.station, station.name).all()
    
    #Close session
    session.close()
    
    # Create a dictionary 
    station_list = []
    for stat, name in station_data:
        station_dict = {stat: name}
        station_list.append(station_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperature():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temperature data
    recent_date = dt.date(2017, 8 , 23)
    year_ago = recent_date - dt.timedelta(days=365)
    date_tobs = session.query(measurement.date, measurement.tobs).filter(measurement.date >= year_ago).\
    filter(measurement.station == "USC00519281").group_by(measurement.date).all() 
    
    #Close session
    session.close()
    
    # Create a dictionary 
    temperature = []
    for date, tobs in date_tobs:
        temperature_dict = {date: tobs}
        temperature.append(temperature_dict)

    return jsonify(temperature)



@app.route("/api/v1.0/<start>")
def temp_by_start_date(start):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Query necessary data
    sel = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    temp_by_start_date = session.query(*sel).filter(measurement.date >= start).all()

    temp_by_start_date_list = []
    for temperature in temp_by_start_date:
        temp_by_start_date_dict = {"Min": temperature[0], "Max": temperature[1], "Avg": temperature[2]}
        temp_by_start_date_list.append(temp_by_start_date_dict)

    return jsonify(temp_by_start_date_list)



if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    