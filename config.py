import os

# Config for os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Secret key for sessions
    # change it before using
    SECRET_KEY = "not_secrEt53454325_SecrT_kEy_chaNGe_8t_bef4re_us8ng_in_pr0duc"

    # File-based SQLite3 database
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app/static/database/VKS_main.sqlite") or \
        "sqlite:///" + os.path.join(basedir, "VKS_Fallback.sqlite")

    # Avoids SQLAlchemy warning (Is usable for Database Debugging at SQLAlchemy)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Elasticsearch Url for Full text search in databse
    ELASTICSEARCH_URL = "http://localhost:9200"

    # Flask-User settings
    USER_APP_NAME = "Communicatio"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True
    USER_ENABLE_CHANGE_USERNAME = True
    USER_ENABLE_CHANGE_PASSWORD = True
    USER_ENABLE_REGISTER = True
    USER_LOGIN_TEMPLATE='flask_user/login_or_register.html'
    USER_REGISTER_TEMPLATE='flask_user/login_or_register.html'

    # Settings for user data validation and databse settings
    USERNAME_MAX_LENGTH = 100
    USERNAME_MIN_LENGTH = 5
    FIRST_NAME_MAX_LENGTH = 100
    FIRST_NAME_MIN_LENGTH = 5
    LAST_NAME_MAX_LENGTH = 100
    LAST_NAME_MIN_LENGTH = 5
    PASSWORD_MIN_LENGTH = 6
    PASSWORD_MAX_LENGTH = 48
