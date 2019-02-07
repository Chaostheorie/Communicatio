import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from elasticsearch import Elasticsearch
from flask_user import UserManager
from flask_babelex import Babel
from flask_migrate import Migrate, upgrade

# Initialize Flask
app = Flask(__name__)

# Load Configuration from Config.py's class "Config"
app.config.from_object(Config)

# Initalize of SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-BabelEx
babel = Babel(app)

# Initialize other things
from app import models

# Initalize Database Migrate
migrate = Migrate(app, db)
try:
    # Autoupgrade if flask migrate is Initialized
    with app.app_context():
        upgrade(directory='migrations', revision='head', sql=False, tag=None)
except:
    pass
# Initalize Elasticsearch
app.elasticsearch = Elasticsearch([app.config["ELASTICSEARCH_URL"]])

# Initalize Search mechanism + mixin
from app import search, mixin

# The session is used for none type objekt transferring (add user, static Users)
# Also for other methods, where an modified session is usefull/ needed
engine = create_engine('sqlite:///app/static/database/VKS_main.sqlite',
 convert_unicode=True or os.path.join(basedir, "VKS_Fallback.sqlite"))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Initalize Routes
from app import routes
