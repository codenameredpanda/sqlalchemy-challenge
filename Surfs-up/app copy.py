# Import the dependencies.

import numpy as np
import pandas as pd
import datetime as dt
import re

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)

# Save references to each table

Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)



