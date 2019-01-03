from flask import *
from app import app
from app.forms import LoginForm

@app.route("/")
def r_log_in():
    return redirect("/log-in")

@app.route("index", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "Post":
        # add search answer with search mixin
        return ""

@app.route('/log-in', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)
