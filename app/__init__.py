from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_user import *
from elasticsearch import Elasticsearch

# Init Flask
app = Flask(__name__)

# Load Configuration from Config.py's class "Config"
app.config.from_object(Config)

# Init of Database modules
db = SQLAlchemy(app)
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \

from app import routes, models
