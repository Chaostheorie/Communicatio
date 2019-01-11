from flask import *
from app import *
from app.mixin import *
from app.models import *
from flask_user import *
from flask_sqlalchemy import *

#setup user manager
user_manager = UserManager(app, db, Users)

# add admin for testing if not added yet
if not Users.query.filter(Users.username == "admin").first():
	user = Users(
		username = "admin",
		password = user_manager.hash_password("Password1"),
		first_name = "Chaostheorie",
		last_name = "https://github.com/Chaostheorie"
    )
	user.roles = [admin_role,]
	db_session.add(user)
	db_session.commit()

# this function is for form Processing
def make_dict(request):
    values = list(request.form.values())
    keys = list(request.form.keys())
    input = {}
    for i in range(len(keys)):
        value = values[i]
        key = keys[i]
        input.update({key:value})
    return input

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        return search_results(request, search)

@app.route("/admin")
@roles_required("Admin")
def admin():
    return render_template("admin.html")

@app.route("/add-user", methods=["POST", "GET"])
@roles_required("Admin")
def add_user():
    if request.method == "GET":
        roles_all = Role.query.order_by(Role.name).all()
        return render_template("add_user.html", roles=roles_all)

    if request.method == "POST":
        user_data = make_dict(request)
        values = list(request.form.values())
        keys = list(request.form.keys())
        input = {}
        for i in range(len(keys)):
            value = values[i]
            key = keys[i]
            input.update({key:value})
        user = Users(
        username=user_data["username"],
        password=user_manager.hash_password(user_data["password"]),
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        )
        # add role with variant of models and a for loop
        print("Peng")
        print(user_data["roles"])
        #	user.roles = [admin_role,]
        #db.session.add(user)
        #db.session.commit()
        return redirect("/add-user")

@app.route("/add-term", methods=["POST", "GET"])
@roles_required("Admin")
def add_term():
    if request.method == "GET":
        return render_template("add_term.html")

    if request.method == "POST":
        new_term = make_dict(request)
        print(new_term)
        return redirect("/add-term")

@app.route("/results")
def search_results(request, search):
    input = make_dict(request)
    text = ""
    if input["type"]=="broadcast":
        entrys.reindex()
        results = query, total = entrys.search(input["search"], 1, 100)
        if input["search"] == "":
                qry = db_session.query(entrys)
                results = qry.all()
                if len(entrys.query.all()) > 1:
                    text = " Es wurden " + str(len(entrys.query.all())) + \
                     " Ergebnisse gefunden:"
                else:
                    text = "Es wurde" + str(len(entrys.query.all())) + \
                     " Ergebniss gefunden: "
                return render_template("results.html", results=results, text=text)

    if input["type"]=="term":
        results = query, total = terms.search(input["search"], 1, 100)
        if input["search"] == "":
                qry = db_session.query(terms)
                results = qry.all()
                if len(terms.query.all()) > 1:
                    text = " Es wurden " + str(len(terms.query.all())) + \
                     " Ergebnisse gefunden:"
                else:
                    text = "Es wurde" + str(len(terms.query.all())) + \
                     " Ergebniss gefunden: "
                return render_template("results.html", results=results, text=text)

    if results[1] > 1:
        text = "Es wurden " + str(total) + " Ergebnisse für den Suchbegriff " +\
         input["search"] + " gefunden:"
    elif results[1] == 1:
        text = "Es wurde 1 Ergebniss für den Suchbegriff " + input["search"] + \
         " gefunden:"
    elif not results:
        print("Pong")
        return redirect("/")
    else:
        flash("Kein Ergebniss für den Suchbegriff " + str(input["search"]) + \
        " gefunden")
        return_url = request.referrer or "/"
        return redirect(return_url)
    return render_template("results.html", results=query, text=text)

# for later implementation and allowing url_for(*) to work
@app.route("/about-us")
def about_us():
    flash("Not Created yet")
    return redirect("/")

@app.route("/all_terms")
def all_terms():
    all = terms.query.all()
    text = "Alle Termine:"
    peter = User.query.filter_by(id=1).all()
    return render_template("terms_results.html", results=all, text=text)

@app.route("/all_entrys")
def all_entrys():
    all = entrys.query.all()
    text = "Alle Einträge:"
    return render_template("results.html", results=all, text=text)#

# Signals form flask user
@user_logged_in.connect_via(app)
def _after_login_hook(sender, user, **extra):
    flash(user.username + " logged in")
    return ""

@user_logged_in.connect_via(app)
def _track_logins(sender, user, **extra):
    #user.last_login_ip = request.remote_addr
    #db.session.commit()
    return ""
