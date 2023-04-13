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
        f"Welcome to Hawaii Weather App<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
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

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for date, prcp in date_prcp:
        passenger_dict = {date: prcp}
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    