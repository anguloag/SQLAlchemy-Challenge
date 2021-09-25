# Import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup and Routes
#################################################

# set Flask app
app = Flask(__name__)

# create Home page - list all routes available
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App Home page!"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/START -- replace START with date in YYYY-MM-DD format<br/>"
        f"/api/v1.0/START/END -- replace START and END with date in YYYY-MM-DD format"
    )

# convert query results to a dictionary 
# - use 'date' as the key, 'prcp' as the value
# - return JSON representation of dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    prcp_measurements_dict = dict(results)
    return jsonify(prcp_measurements_dict)

# return JSON list of stations from dataset
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

# query the dates and tobs of the most active station for the last year of data
# - return JSON list of tobs for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_recent_date = dt.date(2017, 8, 23)
    one_year = dt.timedelta(days=365)
    one_year_before_last = most_recent_date - one_year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_before_last).\
            filter(Measurement.station == 'USC00519281').all()
    session.close()

    tobs_last_year = list(np.ravel(results))
    return jsonify(tobs_last_year)

# return a JSON list of min, avg, and max temp for a given start or start-end range
# - when given start only, calculate TMIN, TAVG, TMAX for all dates greater than or = to start date
# - when given start and end date, calculate TMIN, TAVG, TMAX for dates between start and end, inclusive
@app.route("/api/v1.0/<start>")
def temps_start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    temps_start_data = list(np.ravel(results))
    return jsonify(temps_start_data)

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    temps_start_end_data = list(np.ravel(results))
    return jsonify(temps_start_end_data)


if __name__ == '__main__':
    app.run(debug=True)