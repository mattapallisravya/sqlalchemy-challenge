import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///../resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
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
    
    # Most recent date in the data set.
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date
    
    # Query to retrieve the last 12 months of precipitation data and plot the results. 
    one_year_back_date = dt.date(2017,8,23)- dt.timedelta(days=365)
    print(f"One Year back date = {one_year_back_date}")

    # Query to retrieve the date and precipitation scores
    one_year_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=one_year_back_date).\
            filter(Measurement.date <= latest_date[0]).all()
    
    # Converting list of tuples to dictionary
    #my_dict = dict(one_year_data)

    prec_list=[]
    for date, prcp in one_year_data:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prec_list.append(prcp_dict)

    # Closing the session
    session.close()
    
    # Return Jsonify version of dictionary
    return jsonify(prec_list)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # list all the stations
    stations_list = session.query(Station.station).all()

    # Closing the session
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations_list))

    # Return Jsonify version
    return jsonify(all_stations)

    


    
if __name__ == '__main__':
    app.run(debug=True)
