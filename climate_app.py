from flask import Flask, jsonify
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
app = Flask(__name__)

#prcp_data = pd.read_csv("measurement_data.csv", index_col=0)
#new_dic = list(prcp_data['Precipitation'].to_dict())

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect= True)
Measurements = Base.classes.measurements
session = Session(engine)

@app.route('/api/v1.0/precipitation')
def precipitation():
    data = session.query(Measurements).all()
    final_list = []
    for x in data:
        prcp_list = {}
        prcp_list["Precipitation"] = x.prcp
        prcp_list["Station"] = x.station
        final_list.append(prcp_list)
    return jsonify(final_list)


Stations = Base.classes.stations
@app.route("/api/v1.0/stations")
def stations():
    data2 = session.query(Stations).all()
    final_list2 = []
    for y in data2:
        station_library = {}
        station_library["Station"] = y.station
        final_list2.append(station_library)
    return jsonify(final_list2)

Measurements = Base.classes.measurements
@app.route("/api/v1.0/tobs")
def tobs():
    data3 = session.query(Measurements).all()
    final_list3 = []
    for z in data3:
        tobs_library = {}
        tobs_library["tobs"] = z.tobs
        final_list3.append(tobs_library)
    return jsonify(final_list3)



@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    conn = engine.connect()
    date_and_tobs = conn.execute(" SELECT date, tobs FROM Measurements LEFT JOIN Stations ON Measurements.station = Stations.station WHERE date > '2016-12-31' ").fetchall()
    time_df = pd.DataFrame(date_and_tobs, columns = ["Date", "Tobs"])
    time_df["Date"] = pd.to_datetime(time_df["Date"])

    start_and_finish = time_df[(time_df["Date"] >= start) & (time_df["Date"] <= end)]
    mean = round(np.mean(start_and_finish["Tobs"]), 2)
    minimum = np.min(start_and_finish["Tobs"])
    maximum = np.max(start_and_finish["Tobs"])




    return (" Start date: %s \
              End date: %s \
              Average Temp: %s \
              Max Temp: %s \
              Min Temp: %s " % (start, end, mean, maximum, minimum))
    





if __name__ == '__main__':
    app.run(debug=False)
