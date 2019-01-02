from app import *
from flask import flash, render_template, request, redirect
from models import *
from flask_user import *
from config import ConfigClass
from routes import *

app.run(debug=True, host="0.0.0.0", port=5000)
