from flask import *
from app import app, search, db, db_session
from app.mixin import *
from app.models import entrys, terms
from flask_user import *

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

@app.route("/results")
def search_results(request, search):
    input = make_dict(request)
    text = ""
    # debuging prints fot input checking
    print("Search started")
    print(input)
    print(search)
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
        print("query working")
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
    # must later be used to create terms index for elasticsearch after that
    # could deleted and is replaced in search already with reindex
    for term in terms.query.all():
        add_to_index("terms", term)
        flash("added terms")
    flash("Peng")
    return redirect("/")

@app.route("/all_terms")
def all_terms():
    return ""

@app.route("/all_entrys")
def all_entrys():
    return ""

# Signal if user logged in
# this could later be used for username request or sth like this
@user_logged_in.connect_via(app)
def _after_login_hook(sender, user, **extra):
    flash(user.username + " logged in")
    return ""
