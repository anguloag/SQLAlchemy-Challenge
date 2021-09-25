# Import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import numpy as np
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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# convert query results to a dictionary 
# - use 'date' as the key, 'prcp' as the value
# - return JSON representation of dictionary


# return JSON list of stations from dataset


# query the dates and tobs of the most active station for the last year of data
# - return JSON list of tobs for the previous year


# return a JSON list of min, avg, and max temp for a given start or start-end range
# - when given start only, calculate TMIN, TAVG, TMAX for all dates greater than or = to start date
# - when given start and end date, calculate TMIN, TAVG, TMAX for dates between start and end, inclusive



if __name__ == '__main__':
    app.run(debug=True)