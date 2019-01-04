from flask import *
from app import app
from flask_user import *

@app.route("/")
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "Post":
        # add search answer with search mixin
        return ""

# for later migration and not for url_for("link")
@app.route("/about-us")
def about_us():
    return ""

@app.route("/info")
def Info():
    return ""

@app.route("/all_entrys")
def all_entrys():
    return ""
# Signal for logging if user logged in
@user_logged_in.connect_via(app)
def _after_login_hook(sender, user, **extra):
    flash(user.username + " logged in")
    return ""
