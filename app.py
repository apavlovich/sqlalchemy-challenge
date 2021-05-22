import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

### DATABASE SETUP ###

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

### FLASK SETUP ###

app = Flask(__name__)

### FLASK ROUTES ###

@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate API!<br/><br/>"
        f"Available Routes:<br/><br/>"
        f"Precipitation (inches) from the last year of data:<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"A list of stations:<br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"Dates and tempatures from the most active station from the last year of data:<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"Tempature stats for dates starting at the given start date inclusive:<br/>"
        f"Date format: YYYY-MM-DD<br/>"
        f"/api/v1.0/start date<br/><br/>"
        f"Tempature stats for dates in between the given start and end date inclusive:<br/>"
        f"Date format: YYYY-MM-DD<br/>"
        f"/api/v1.0/start date/end date"
    )

#############################################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= "2016-08-23").all()
    session.close()

    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

#############################################################################################

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).\
                    order_by(Station.station).all()
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#############################################################################################

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= "2016-08-23").\
                    filter(Measurement.station == "USC00519281").all()
    session.close()

    all_tobs = list(np.ravel(results))
    
    return jsonify(all_tobs)

#############################################################################################

@app.route("/api/v1.0/<start>")
def min_avg_max_start(start):
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), 
                            func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                            filter(Measurement.date >= start).group_by(Measurement.date).all()
    session.close()
    
    all_tobs = []
    for date, min, avg, max in results:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['Min'] = min
        tobs_dict['Avg'] = avg
        tobs_dict['Max'] = max
        all_tobs.append(tobs_dict)
        
    return jsonify(all_tobs)

#############################################################################################

@app.route("/api/v1.0/<start>/<end>")
def min_avg_max_start_end(start, end):
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs),
                            func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                            filter((Measurement.date >= start) & (Measurement.date <= end)).\
                            group_by(Measurement.date).all()
    session.close()

    all_tobs = []
    for date, min, avg, max in results:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['Min'] = min
        tobs_dict['Avg'] = avg
        tobs_dict['Max'] = max
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)

#############################################################################################

if __name__ == '__main__':
    app.run(debug=True)