import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import Date, cast, func

import datetime as dt
from datetime import date, datetime

from flask import Flask, jsonify

# database setup
#################################################
# create engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare base and automap
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# assign to variables
measurement = Base.classes.measurement
station = Base.classes.station

# create session
session = Session(engine)

# Flask Setup
#################################################
app = Flask(__name__)


# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Date format = mm-dd-yyyy <br/>"
        f"/api/v1.0/'<start>'<br/>"
        f"/api/v1.0/'<start>'/'<end>'<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for the dates and precipitation from the last year.
    # Convert the query results to a Dictionary using date as the key and
    # precipiation as the value.
    # Return the json representation of your dictionary.
    today = date.today()
    date12today = today - dt.timedelta(days=365 * 2)
    d12 = date12today.isoformat()

    data = session.query(measurement.prcp, measurement.date).\
        order_by(measurement.date.desc()).\
        filter(measurement.date >= d12).all()

    answer = []
    for a in range(len(data)):
        bar = {}
        bar[str(data[a][1])] = data[a][0]
        answer.append(bar)

    return jsonify(answer)


@app.route("/api/v1.0/stations")
def stations():
    # Return a json list of stations from the dataset.    today = date.today()
    StationName = session.query(station.station).all()

    return jsonify(StationName)


@app.route("/api/v1.0/tobs")
def tobs():
    # Return a json list of stations from the dataset.    today = date.today()
    today = date.today()
    date12today = today - dt.timedelta(days=365 * 2)
    d12 = date12today.isoformat()

    data = session.query(measurement.tobs).\
        filter(measurement.date >= d12).all()

    return jsonify(data)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end=None):
    date1 = datetime.strptime(start, '%m-%d-%Y').isoformat()
    if end:
        date2 = datetime.strptime(end, '%m-%d-%Y').isoformat()

    maxT = session.query(func.max(measurement.tobs)).\
        filter(measurement.date >= date1)
    if end:
        maxT = maxT.filter(measurement.date <= date2)
    maxT = maxT.all()

    minT = session.query(func.min(measurement.tobs)).\
        filter(measurement.date >= date1)
    if end:
        minT = minT.filter(measurement.date <= date2)
    minT = minT.all()

    avgT = session.query(func.avg(measurement.tobs)).\
        filter(measurement.date >= date1)
    if end:
        avgT = avgT.filter(measurement.date <= date2)
    avgT = avgT.all()

    data = {"Date": date1 + " " + date2 if end else date1,
        "Temp, Max": maxT[0][0],
        "Temp, Min": minT[0][0],
        "Temp, Avg": round(avgT[0][0], 2)}

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
