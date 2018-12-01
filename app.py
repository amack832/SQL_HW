import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
#################################################
app = Flask(__name__)

#Home page with routes to the specific task/info
@app.route("/")
def home():
    print("Server request for Home")
    return(f"Hawaii Weather API<br>"
           f"Available Routes:<br>"
           f"/api/v1.0/precipitation<br>"
           f"/api/v1.0/stations<br>"
           f"/api/v1.0/tobs<br><br>"
           f"/api/v1.0/<start><br>"
           f"/api/v1.0/<start>/<end><br>")

#Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    p_data_date = session.query(Measurement.date).filter(Measurement.date >= "2016-08-23").all()
    p_data_prcp = session.query(Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()

    p_date_list = list(np.ravel(p_data_date))
    p_prcp_list = list(np.ravel(p_data_prcp))

    precip_dict = dict(zip(p_date_list, p_prcp_list))

    return jsonify(precip_dict)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    stations_data = session.query(Station.station).all()

    stations = list(np.ravel(stations_data))

    return jsonify(stations)

#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_data = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23")

    tobs = list(np.ravel(tobs_data))

    return jsonify(tobs)

#Tried many times with the start dates. Kept telling me there was key error.

if __name__ == '__main__':
    app.run(debug=True)
