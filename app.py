# import Flask
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from flask import Flask, jsonify

# Database set up
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Setup
app = Flask(__name__)

# List all routes that are available
@app.route("/")
def Home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Convert the query results to a dictionary

@app.route("/api/v1.0/precipitation")
def date_prcp():
    session =  Session(engine)
    result = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    date_prcp = list(np.ravel(result))
    return jsonify(date_prcp)

# Return a JSON list of stations from the dataset

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    result_s = session.query(Station.station).all()
    session.close()
    station = list(np.ravel(result_s))
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    result_t = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").all()
    session.close()
    tobs = list(np.ravel(result_t))
    return jsonify(tobs)

@app.route("/api/v1.0/2017-01-01")
def start_date_t():
    session = Session(engine)
    
    min = session.query(Measurement.tobs, func.min(Measurement.tobs)).filter(Measurement.date > "2017-01-01").all()
    max = session.query(Measurement.tobs, func.max(Measurement.tobs)).filter(Measurement.date > "2017-01-01").all()
    avg = session.query(Measurement.tobs, func.avg(Measurement.tobs)).filter(Measurement.date > "2017-01-01").all()
    result_sd = (min, max, avg)
    session.close()
    start_date_t = list(np.ravel(result_sd))
    return jsonify(start_date_t)

@app.route("/api/v1.0/2017-01-01/2017-06-01")
def end_date_t():
    session = Session(engine)
    
    min = session.query(Measurement.tobs, func.min(Measurement.tobs)).filter(Measurement.date > "2017-01-01").filter(Measurement.date < "2017-06-01").all()
    max = session.query(Measurement.tobs, func.max(Measurement.tobs)).filter(Measurement.date > "2017-01-01").filter(Measurement.date < "2017-06-01").all()
    avg = session.query(Measurement.tobs, func.avg(Measurement.tobs)).filter(Measurement.date > "2017-01-01").filter(Measurement.date < "2017-06-01").all()
    result_ed = (min, max, avg)
    session.close()
    end_date_t = list(np.ravel(result_ed))
    return jsonify(end_date_t)

if __name__ == "__main__":
    app.run(debug=True)

    