import os
from flask import Flask
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from elasticsearch import Elasticsearch
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask
app = Flask(__name__)

# Load Configuration from Config.py's class "Config"
app.config.from_object(Config)

# Initalize of SQLAlchemy
db = SQLAlchemy(app)
# The session object is replaced with a custom session, because the custom
# Session allows to use enable transaction of None Type objects for user Obj
# Without overwritting flask sqlalchemy
engine = create_engine('sqlite:///app/static/database/VKS_main.sqlite',
    convert_unicode=True or os.path.join(basedir, "VKS_Fallback.sqlite"))
db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))

# Initialize Flask-BabelEx
babel = Babel(app)

# Initialize other things
from app import models

# Initalize of flask user
from app.custom import *
from app.models import User
user_manager = CustomUserManager(app, db, User)

# Initalize Database Migrate if set to True in Config
# At default it's set at False and must be manually activated
# A guideline is at the github wiki
if app.config["FLASK_MIGRATE"] == True:
    from flask_migrate import Migrate, upgrade
    migrate = Migrate(app, db)
    try:
        # try to Autoupgrade if flask migrate is activated
        with app.app_context():
            upgrade(directory='migrations', revision='head', sql=False, tag=None)
    except:
        pass
else:
    pass

# Initalize Elasticsearch
app.elasticsearch = Elasticsearch([app.config["ELASTICSEARCH_URL"]])

# Initalize Search mechanism + mixin
from app import search, mixin

# reindex
from app.models import User, entrys, terms
User.reindex()
entrys.reindex()
terms.reindex()

# Initalize Routes
from app import routes
