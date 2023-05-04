import io
from application import app
from flask import jsonify, make_response, render_template, request, url_for
from datetime import datetime
import pandas as pd
import psycopg2 as ps
import os
import json
import plotly
import plotly.express as px
import csv

# Get Postgres credentials from environment variables
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_DB = os.environ['POSTGRES_DB']

# Connect to Postgres database
conn = ps.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    database=POSTGRES_DB
)

# Define route for temperature data
@app.route('/temperature')
def temperature(start_time=None, end_time=None):
    cur = conn.cursor()
    if start_time and end_time:
        cur.execute("SELECT time, value FROM public.\"CM_HAM_DO_AI1/Temp_value\" WHERE time BETWEEN %s AND %s", (start_time, end_time))
    else:
        cur.execute("SELECT time, value FROM public.\"CM_HAM_DO_AI1/Temp_value\"")
    rows = cur.fetchall()
    data = {
        'time': [datetime(row[0].year, row[0].month, row[0].day, row[0].hour, row[0].minute, row[0].second, row[0].microsecond) for row in rows],
        'value': [row[1] for row in rows]
    }
    figT = px.line(data, x='time', y='value', title='Temperature over Time')
    graphTJSON = json.dumps(figT.to_dict(), cls = plotly.utils.PlotlyJSONEncoder)
    return graphTJSON


# Define route for temperature data with timeframe
@app.route('/get_chart_data_t')
def get_chart_data_t():
    # Get the start and end time parameters from the request
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Convert the start and end time strings to datetime objects
    if start_time and end_time:
        start_time = datetime.fromisoformat(start_time.replace('T', ' '))
        end_time = datetime.fromisoformat(end_time.replace('T', ' '))
    else:
        start_time = None
        end_time = None

    # Call the temperature function with the start and end time parameters
    graphTJSON = temperature(start_time, end_time)
    # Return the chart data as JSON
    return graphTJSON


# Define route for downloading temperature data as CSV file
@app.route('/download_csv_t')
def download_csv_t():
    try:
        cur = conn.cursor()
        cur.execute("SELECT time, value FROM public.\"CM_HAM_DO_AI1/Temp_value\"")
        rows = cur.fetchall()
        data = [[row[0].strftime('%Y-%m-%d %H:%M:%S.%f'), row[1]] for row in rows]
        response = make_response('')
        response.headers["Content-Disposition"] = "attachment; filename=temperature_data.csv"

        # write data to StringIO buffer
        with io.StringIO() as buffer:
            writer = csv.writer(buffer)
            writer.writerow(['time', 'value'])
            writer.writerows(data)
            response.data = buffer.getvalue()
        response.mimetype='text/csv'
        return response
    except Exception as e:
        print(f"Error in download_csv function: {e}")
        return None
    

# Define route for pH data
@app.route('/ph')
def ph(start_time=None, end_time=None):
    cur = conn.cursor()
    if start_time and end_time:
        cur.execute("SELECT time, value FROM public.\"CM_HAM_PH_AI1/pH_value\" WHERE time BETWEEN %s AND %s", (start_time, end_time))
    else:
        cur.execute("SELECT time, value FROM public.\"CM_HAM_PH_AI1/pH_value\"")
    rows = cur.fetchall()
    data = {
        'time': [datetime(row[0].year, row[0].month, row[0].day, row[0].hour, row[0].minute, row[0].second, row[0].microsecond) for row in rows],
        'value': [row[1] for row in rows]
    }
    figPH = px.line(data, x='time', y='value', title='pH over Time')
    graphPHJSON = json.dumps(figPH.to_dict(), cls = plotly.utils.PlotlyJSONEncoder)
    return graphPHJSON


# Define route for pH data with timeframe
@app.route('/get_chart_data_ph')
def get_chart_data_ph():
    # Get the start and end time parameters from the request
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Convert the start and end time strings to datetime objects
    if start_time and end_time:
        start_time = datetime.fromisoformat(start_time.replace('T', ' '))
        end_time = datetime.fromisoformat(end_time.replace('T', ' '))
    else:
        start_time = None
        end_time = None

    # Call the ph function with the start and end time parameters
    graphPHJSON = ph(start_time, end_time)
    # Return the chart data as JSON
    return graphPHJSON


# Define route for downloading ph data as CSV file
@app.route('/download_csv_ph')
def download_csv_ph():
    try:
        cur = conn.cursor()
        cur.execute("SELECT time, value FROM public.\"CM_HAM_PH_AI1/pH_value\"")
        rows = cur.fetchall()
        data = [[row[0].strftime('%Y-%m-%d %H:%M:%S.%f'), row[1]] for row in rows]
        response = make_response('')
        response.headers["Content-Disposition"] = "attachment; filename=ph_data.csv"
        
        # write data to StringIO buffer
        with io.StringIO() as buffer:
            writer = csv.writer(buffer)
            writer.writerow(['time', 'value'])
            writer.writerows(data)
            response.data = buffer.getvalue()
        response.mimetype='text/csv'
        return response
    except Exception as e:
        print(f"Error in download_csv function: {e}")
        return None


# Define route for distilled oxygen data
@app.route('/distilled-oxygen')
def distilled_oxygen(start_time=None, end_time=None):
    cur = conn.cursor()
    if start_time and end_time:
        cur.execute("SELECT time, value FROM public.\"CM_PID_DO/Process_DO\" WHERE time BETWEEN %s AND %s", (start_time, end_time))
    else:
        cur.execute("SELECT time, value FROM public.\"CM_PID_DO/Process_DO\"")
    rows = cur.fetchall()
    data = {
        'time': [datetime(row[0].year, row[0].month, row[0].day, row[0].hour, row[0].minute, row[0].second, row[0].microsecond) for row in rows],
        'value': [row[1] for row in rows]
    }
    figDO = px.line(data, x='time', y='value', title='Distilled Oxygen over Time')
    graphDOJSON = json.dumps(figDO.to_dict(), cls = plotly.utils.PlotlyJSONEncoder)
    return graphDOJSON


# Define route for distilled oxygen data with timeframe
@app.route('/get_chart_data_do')
def get_chart_data_do():
    # Get the start and end time parameters from the request
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Convert the start and end time strings to datetime objects
    if start_time and end_time:
        start_time = datetime.fromisoformat(start_time.replace('T', ' '))
        end_time = datetime.fromisoformat(end_time.replace('T', ' '))
    else:
        start_time = None
        end_time = None

    # Call the distilled_oxygen function with the start and end time parameters
    graphDOJSON = distilled_oxygen(start_time, end_time)
    # Return the chart data as JSON
    return graphDOJSON


# Define route for downloading distilled oxygen data as CSV file
@app.route('/download_csv_do')
def download_csv_do():
    try:
        cur = conn.cursor()
        cur.execute("SELECT time, value FROM public.\"CM_PID_DO/Process_DO\"")
        rows = cur.fetchall()
        data = [[row[0].strftime('%Y-%m-%d %H:%M:%S.%f'), row[1]] for row in rows]
        response = make_response('')
        response.headers["Content-Disposition"] = "attachment; filename=distilled_oxygen_data.csv"
        
        # write data to StringIO buffer
        with io.StringIO() as buffer:
            writer = csv.writer(buffer)
            writer.writerow(['time', 'value'])
            writer.writerows(data)
            response.data = buffer.getvalue()
        response.mimetype='text/csv'
        return response
    except Exception as e:
        print(f"Error in download_csv function: {e}")
        return None


# Define route for pressure data
@app.route('/pressure')
def pressure(start_time=None, end_time=None):
    cur = conn.cursor()
    if start_time and end_time:
        cur.execute("SELECT time, value FROM public.\"CM_PRESSURE/Output\" WHERE time BETWEEN %s AND %s", (start_time, end_time))
    else:
       cur.execute("SELECT time, value FROM public.\"CM_PRESSURE/Output\"")
    rows = cur.fetchall()
    data = {
        'time': [datetime(row[0].year, row[0].month, row[0].day, row[0].hour, row[0].minute, row[0].second, row[0].microsecond) for row in rows],
        'value': [row[1] for row in rows]
    }
    figP = px.line(data, x='time', y='value', title='Pressure over Time')
    graphPJSON = json.dumps(figP.to_dict(), cls = plotly.utils.PlotlyJSONEncoder)
    return graphPJSON


# Define route for pressure data with timeframe
@app.route('/get_chart_data_p')
def get_chart_data_p():
    # Get the start and end time parameters from the request
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Convert the start and end time strings to datetime objects
    if start_time and end_time:
        start_time = datetime.fromisoformat(start_time.replace('T', ' '))
        end_time = datetime.fromisoformat(end_time.replace('T', ' '))
    else:
        start_time = None
        end_time = None

    # Call the pressure function with the start and end time parameters
    graphPJSON = pressure(start_time, end_time)
    # Return the chart data as JSON
    return graphPJSON


# Define route for downloading pressure data as CSV file
@app.route('/download_csv_p')
def download_csv_p():
    try:
        cur = conn.cursor()
        cur.execute("SELECT time, value FROM public.\"CM_PRESSURE/Output\"")
        rows = cur.fetchall()
        data = [[row[0].strftime('%Y-%m-%d %H:%M:%S.%f'), row[1]] for row in rows]
        response = make_response('')
        response.headers["Content-Disposition"] = "attachment; filename=pressure_data.csv"
        
        # write data to StringIO buffer
        with io.StringIO() as buffer:
            writer = csv.writer(buffer)
            writer.writerow(['time', 'value'])
            writer.writerows(data)
            response.data = buffer.getvalue()
        response.mimetype='text/csv'
        return response
    except Exception as e:
        print(f"Error in download_csv function: {e}")
        return None
    

@app.route('/')
def index():
    graphTJSON = temperature()
    graphPHJSON = ph()
    graphDOJSON = distilled_oxygen()
    graphPJSON = pressure()
    return render_template("index.html", title = "Home", graphTJSON = graphTJSON, 
                           graphPHJSON = graphPHJSON, graphDOJSON = graphDOJSON,
                           graphPJSON = graphPJSON)