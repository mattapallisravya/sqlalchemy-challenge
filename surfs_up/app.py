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
        f"Enter below URL along with required start date Eg:/api/v1.0/2016-08-23<br/>"
        f"date format: YYYY-MM-DD, data available is between 2010-01-01 and 2017-08-23.<br/>"
        f"/api/v1.0/<start><br/>"
        f"Enter below URL along with required start date and end date Eg:/api/v1.0/2016-08-23/2017-08-23<br/>"
        f"date format: YYYY-MM-DD, data available is between 2010-01-01 and 2017-08-23.<br/>"
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

# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to find the most active stations (i.e. what stations have the most rows?)
    active_station = session.query(Measurement.station,func.count(Measurement.station)).\
            group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    active_station

    # Most active station
    most_active_station = active_station[0][0]
    most_active_station

    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    latest_date = session.query(Measurement.date).filter(Measurement.station ==most_active_station ).order_by(Measurement.date.desc()).first()
    latest_date
    one_year_back_date = dt.date(2017,8,18)- dt.timedelta(days=365)
    one_year_back_date
    temp = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>=one_year_back_date).\
        filter(Measurement.date<=latest_date[0]).all()

     # Closing the session
    session.close()

    # Convert list of tuples into normal list
    all_stations_temp = list(np.ravel(temp))

    # Return Jsonify version
    return jsonify(all_stations_temp)

#Return a JSON list of the minimum temperature, the average temperature, 
# and the maximum temperature for a specified start.
@app.route("/api/v1.0/<start>")
def start_date_temp_calc(start):
       
        # Create our session (link) from Python to the DB
        session = Session(engine)

        #start = dt.datetime.strptime(start, "%m-%d-%Y")
        
        # query the database to min, max, avg temp
        temp_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs)\
                    ,func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()

        # Closing the session
        session.close()
        

        # Convert list of tuples into normal list
        temp_statss = list(np.ravel(temp_stats))
        
        #if start == Measurement.date:
            # Return Jsonify version
        return jsonify(f"Min Temperature:{temp_statss[0]}, Max Temperature:{temp_statss[1]}, Average Temperature:{temp_statss[2]} ")
        # else:
        # return jsonify({"error":f"{start} is not matching records"}),404
        
    
#Return a JSON list of the minimum temperature, the average temperature, 
# and the maximum temperature for a specified start-end range.
@app.route("/api/v1.0/<start>/<end>")
def start_end_date_temp_calc(start,end):
       
        # Create our session (link) from Python to the DB
        session = Session(engine)

        #start = dt.datetime.strptime(start, "%m-%d-%Y")
        
        # query the database to min, max, avg temp
        temp_stat = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs)\
                    ,func.avg(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()

        # Closing the session
        session.close()
        

        # Convert list of tuples into normal list
        temp_st = list(np.ravel(temp_stat))
        
        #if start == Measurement.date:
            # Return Jsonify version
        return jsonify(f"Min Temperature:{temp_st[0]}, Max Temperature:{temp_st[1]}, Average Temperature:{temp_st[2]} ")
        # else:
        # return jsonify({"error":f"{start} is not matching records"}),404
        

if __name__ == '__main__':
    app.run(debug=True)
