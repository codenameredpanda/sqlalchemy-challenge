import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawai'i Climate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_query = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year).all()

    session.close()
    precip = {date: prcp for date, prcp in precip_query}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    stat_query = session.query(*sel).all()

    session.close()

    stations = []
    for station, name, latitude, longitude, elevation in stat_query:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        stations.append(station_dict)
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   
    tobs_query = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year).all()

    session.close()

    temps = []
    for date, tobs in tobs_query:
        tobs_dict = {}
        tobs_dict ['date'] = date
        tobs_dict ['tobs'] = tobs
        temps.append(tobs_dict)
    
    return jsonify(temps)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_info():
    """Return TMIN, TAVG, TMAX."""
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        start = dt.datetime.strptime(start, "%m-%d-%Y")
        query = session.query(*sel).\
            filter(Measurement.date >= start).all()

        session.close()

        temps = []
        for avg_temp, max_temp, min_temp in query:
            tobs_dict = {}
            tobs_dict ['Average Temp'] = avg_temp
            tobs_dict ['Maximum Temp'] = max_temp
            tobs_dict ['Minimum Temp'] = min_temp
            temps.append(tobs_dict)
        return jsonify(temps)

    start = dt.datetime.strptime(start, "%m-%d-%Y")
    end = dt.datetime.strptime(end, "%m-%d-%Y")

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    temps = []
    for avg_temp, max_temp, min_temp in query:
        tobs_dict = {}
        tobs_dict ['Average Temp'] = avg_temp
        tobs_dict ['Maximum Temp'] = max_temp
        tobs_dict ['Minimum Temp'] = min_temp
        temps.append(tobs_dict)
    return jsonify(temps)

if __name__ == '__main__':
    app.run()


