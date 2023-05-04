
## Introduction

This is a web-based data visualization tool built using Python, Flask, and Plotly with a front-end built with HTML, CSS, and JavaScript to display time-series data of temperature, pressure, pH, and distilled oxygen based on a specific dataset. It also consists of data filtering based on user-provided start and end time and allowed downloading of data in CSV format. It uses PostgreSQL database schema to efficiently store and query large amounts of sensor data. The application is containerized using Docker and deployed on an AWS EC2 instance.

## Technical Details

In this directory, you'll find a `Dockerfile` that defines the image your code will be copied into and installed in. Specifically, the source code will be installed into a Python 3.10 virtual environment as a package via pip, along with any dependencies specified in a `requirements.txt` file.

You'll also find a `compose.yaml` file that defines the container that'll be used to run your code. Specifically, to serve your web-based dashboard in a local browser at http://localhost:8888/, Docker is configured to start the container by executing `run.py`, the expected [entrypoint](https://setuptools.pypa.io/en/latest/userguide/entry_point.html) for your application.

### The database

The data being visualizing is in a Postgres database, also configured in `compose.yaml`.

### The data

The tables in the database:
```
brx1=# \dt

                      List of relations
 Schema |           Name           | Type  |      Owner       
--------+--------------------------+-------+------------------
 public | CM_HAM_DO_AI1/Temp_value | table | process_trending
 public | CM_HAM_PH_AI1/pH_value   | table | process_trending
 public | CM_PID_DO/Process_DO     | table | process_trending
 public | CM_PRESSURE/Output       | table | process_trending
 ```

Each table has the same schema, like so:
```
brx1=# \d public."CM_HAM_DO_AI1/Temp_value"

                Table "public.CM_HAM_DO_AI1/Temp_value"
 Column |            Type             | Collation | Nullable | Default 
--------+-----------------------------+-----------+----------+---------
 time   | timestamp without time zone |           |          | 
 value  | double precision            |           |          | 
```

Each table contains the following data:

| Table                    | Name             | Units   |
|--------------------------|------------------|---------|
| CM_HAM_DO_AI1/Temp_value | Temperature      | Celsius |
| CM_HAM_PH_AI1/pH_value   | pH               | n/a     |
| CM_PID_DO/Process_DO     | Distilled Oxygen | %       |
| CM_PRESSURE/Output       | Pressure         | psi     |

