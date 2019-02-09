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

# The session is used for none type objekt transferring (add user, static Users)
# Also for other methods, where an modified session is usefull/ needed
engine = create_engine('sqlite:///app/static/database/VKS_main.sqlite',
 convert_unicode=True or os.path.join(basedir, "VKS_Fallback.sqlite"))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Initalize Routes
from app import routes
