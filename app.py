import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)
# * `/`

#   * Home page.

#   * List all routes that are available.
### Routes
@app.route("/")
def homepage():
    """List of all returnable API routes."""
    return(
        f"(Note: Dates range from 2010-01-01 to 2017-08-23). <br><br>"
        f"Available Routes: <br>"

        f"/api/v1.0/precipitation<br/>"
        f"Returns dates and temperature from the last year. <br><br>"

        f"/api/v1.0/stations<br/>"
        f"Returns a json list of stations. <br><br>"

        f"/api/v1.0/tobs<br/>"
        f"Returns list of Temperature Observations(tobs) for previous year. <br><br>"

        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"Returns an Average, Max, and Min temperatures for a given start date.<br><br>"

        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"Returns an Average, Max, and Min temperatures for a given date range."
    )
  
# * `/api/v1.0/precipitation`
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return Dates and Temp from the last year."""
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24", Measurement.date <= "2017-08-23").\
        all()
# * Return the JSON representation of your dictionary.
    precipitation_list = [results]

    return jsonify(precipitation_list)

# * `/api/v1.0/stations`
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    results = session.query(Station.name, Station.station, Station.elevation).all()
#   * Return a JSON list of stations from the dataset.
    station_list = []
    for result in results:
        row = {}
        row['name'] = result[0]
        row['station'] = result[1]
        row['elevation'] = result[2]
        station_list.append(row)
    return jsonify(station_list)

# * `/api/v1.0/tobs`
#   * query for the dates and temperature observations from a year from the last data point.
@app.route("/api/v1.0/tobs")
def temp_obs():
    """Return a list of tobs for the previous year"""
    results = session.query(Station.name, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24", Measurement.date <= "2017-08-23").\
        all()
#   * Return a JSON list of Temperature Observations (tobs) for the previous year.
    tobs_list = []
    for result in results:
        row = {}
        row["Station"] = result[0]
        row["Date"] = result[1]
        row["Temperature"] = int(result[2])
        tobs_list.append(row)
# * `/api/v1.0/<start>` 
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route('/api/v1.0/<start>')
def query_dates(start_date):
    """Return the avg, max, min, temp over a specific start date"""
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date.
    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["Average Temperature"] = float(result[0])
        row["Max Temperature"] = float(result[1])
        row["Minimum Temperature"] = float(result[2])
        data_list.append(row)
    return jsonify(data_list)

# and `/api/v1.0/<start>/<end>`
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):
    """Return the avg, max, min, temp over a specific time period"""
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = float(result[0])
        row["Max Temperature"] = float(result[1])
        row["Minimum Temperature"] = float(result[2])
        data_list.append(row)
    return jsonify(data_list)
# finish
if __name__ == '__main__':
    app.run(debug=True)