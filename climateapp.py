import sqlalchemy
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

app = Flask(__name__)


engine = create_engine("sqlite:///hawaii.sqlite")


Base = automap_base()


Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station


session = Session(engine)


@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return a list of measurement date and precipitation information from the last year """
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)
    
    
    precipitation_values = []
    for p in results:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        precipitation_values.append(prcp_dict)

    return jsonify(precipitation_values)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station names"""
    
    results = session.query(Station.name).all()

    
    station_names = list(np.ravel(results))

    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all temperature observations for the previous year"""
    
    results = session.query(Measurement.tobs).all()


    tobs_values = list(np.ravel(results))

    return jsonify(tobs_values)


@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    """ Given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than 
        and equal to the start date. 
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    

    temperatures_start = list(np.ravel(results))

    return jsonify(temperatures_start)


@app.route("/api/v1.0/<start>/<end>")
def temperatures_start_end(start, end):
    """ When given the start and the end date, calculate the TMIN, TAVG, 
        and TMAX for dates between the start and end date inclusive.
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    

    temperatures_start_end = list(np.ravel(results))

    return jsonify(temperatures_start_end)


if __name__ == "__main__":
    app.run(debug=True)