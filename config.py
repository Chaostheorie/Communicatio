import os
# import os for the case you want to check if there is any app.config variables
# already set in the main.py with os.environ.get("variable name") for config

# Config class for Apps (flask_sqlalchemy, flask_user, elasticsearch)
class ConfigClass(object):
	# File-based SQLite3 database
	SQLALCHEMY_DATABASE_URI = 'sqlite:///static/database/VKS.sqlite'
	# Avoids SQLAlchemy warning (Can Help by Database Processing Debugging)
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	# *Not Secret* Secret Key do not use in production
	SECRET_KEY = 'Secret Key is a config for session'
	# Flask-User settings for Auth
	USER_APP_NAME = "Communicatio"
	USER_ENABLE_EMAIL = False
	USER_ENABLE_USERNAME = True
	USER_ENABLE_CHANGE_USERNAME = False
	USER_ENABLE_CHANGE_PASSWORD = True
	USER_ENABLE_REGISTER = False
	# Elasticsearch Url for Full text search
	ELASTICSEARCH_URL = "http://localhost:9200"
