from flask import *
from app import *
from app.mixin import *
from app.models import *
from flask_user import *
from flask_sqlalchemy import *
import time

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
    user.roles.append(Roles(name="Admin"))
    db.session.add(user)
    db.session.commit()

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
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        type = "specific"
        spdict = ""
        return search_results(request, type, spdict)

@app.route("/admin")
@roles_required("Admin")
def admin():
    return render_template("admin.html")

@app.route("/add-user", methods=["POST", "GET"])
@roles_required("Admin")
def add_user():
    if request.method == "GET":
        roles_all = Roles.query.order_by(Roles.name).all()
        return render_template("add_user.html", roles=roles_all)

    if request.method == "POST":
        multiselect = request.form.getlist("roles")
        user1 = Users(
        username = request.form["username"],
        password = user_manager.hash_password(request.form["password"]),
        first_name = request.form["first_name"],
        last_name = request.form["last_name"],
        )
        for i in range(len(multiselect)):
            user1.roles.append(Roles(name=multiselect[i]))
            print(str(i) + ": " + multiselect[i])
        db.session.add(user1)
        db.session.commit()
        flash("Add username: " + request.form["username"] + " sucessfully")
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

@app.route("/logins_views")
@roles_required("Admin")
def logins_view():
    return ""

@app.route("/results")
@login_required
def search_results(request, type, spdict):
    if type == "specific":
        input = make_dict(request)

    elif type == "nonspecific":
        input = spdict

    else:
        flash("Error 02: Bad request")
        return redirect("/")

    print(input)

    if input["type"]=="broadcast":
        result_type = input["type"] or ""
        entrys.reindex()
        results = query, total = entrys.search(input["search"], 1, 100)
        if input["search"] == "":
                qry = db_session.query(entrys)
                results = qry.all()
                for res in results:
                    author_id = res.id
                author = Users.query.filter_by(id=author_id).first()
                if len(entrys.query.all()) > 1:
                    text = " Es wurden " + str(len(entrys.query.all())) + \
                     " Ergebnisse gefunden:"
                else:
                    text = "Es wurde " + str(len(entrys.query.all())) + \
                     " Ergebniss gefunden: "

                return render_template("results.html", results=results, \
                text=text, result_type=result_type, author_name=author.username)

    if input["type"]=="term":
        terms.reindex()
        results = query, total = terms.search(input["search"], 1, 100)
        result_type = input["type"] or ""
        if input["search"] == "":
                qry = db_session.query(terms)
                results = qry.all()
                if len(terms.query.all()) > 1:
                    text = " Es wurden " + str(len(terms.query.all())) + \
                     " Ergebnisse gefunden:"
                else:
                    text = "Es wurde " + str(len(terms.query.all())) + \
                     " Ergebniss gefunden: "
                return render_template("results.html", results=results, text=text, result_type=result_type)

    if results[1] > 1:
        text = "Es wurden " + str(total) + " Ergebnisse für den Suchbegriff " +\
         input["search"] + " gefunden:"
    elif results[1] == 1:
        text = "Es wurde 1 Ergebniss für den Suchbegriff " + input["search"] + \
         " gefunden:"
    elif not results:
        flash("Database Failure 01 - no FTS index or search data")
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
    return_url = request.referrer or "/"
    return redirect(return_url)

@app.route("/profile/<username>")
@login_required
def profile(username):
    user = Users.query.filter_by(username=username).first_or_404()
    return render_template("profile.html", user=user )

@app.route("/all_terms")
@login_required
def all_terms():
    request = ""
    spdict = {'search': '', 'type': 'term'}
    type = "nonspecific"
    return search_results(request, type, spdict)

@app.route("/all_entrys")
@login_required
def all_entrys():
    request = ""
    spdict = {'search': '', 'type': 'broadcast'}
    type = "nonspecific"
    return search_results(request, type, spdict)

@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    if request.method == "GET":
        return render_template("report.html")

    if request.method == "POST":
        make_dict(request)
        return ""

# Signals form flask user
@user_logged_in.connect_via(app)
def _after_login_hook(sender, user, **extra):
    flash(user.username + " logged in")
    return ""

@user_logged_in.connect_via(app)
def _track_logins(sender, user, **extra):
    user.last_login_ip = request.remote_addr
    login = logins(
    ip = user.last_login_ip,
    user_id = user.id,
    time = time.asctime(),
    )
    db.session.add(login)
    db.session.commit()
    return ""

# Errorhandler pages
@app.errorhandler(404)
def page_not_found(e):
    return_url = request.referrer or "/"
    er = "404"
    return render_template("error.html", return_url=return_url, error=er), 404

@app.errorhandler(403)
def forbidden(e):
    return_url = request.referrer or "/"
    er = "403"
    return render_template("error.html", return_url=return_url, error=er), 403
