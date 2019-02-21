from flask import *
from app import *
from app.mixin import *
from app.models import *
from flask_user import *
from app.custom import *
from flask_sqlalchemy import *
import time, datetime

# Check if admin and guest User already exists
if not User.query.filter(User.username == "Admin").all():
    # If it doesn't the admin user will be created
    user = User(
        username = "Admin",
        password = user_manager.hash_password("Password1"),
        first_name = "Chaostheorie",
        last_name = "Admin",
        level = "admin",
        level_specific = "Staff of VKS",
        description = "The admin of the Project."
    )
    user.roles.append(Role(name="Admin"))
    db.session.add(user)
    db.session.commit()
if app.config["GUEST_USER"] == True:
    if not User.query.filter(User.username == "guest").all():
        user = User(
            username = "guest",
            password = user_manager.hash_password("Passwort"),
            first_name = "Gast",
            last_name = "Coder Dojo",
            level = "pupil",
            school_class = "10B",
            description = "Anonymous guest user"
            )
        db.session.add(user)
        db.session.commit()

elif app.config["GUEST_USER"] == False:
    if not User.query.filter(User.username == "guest").all():
        pass
    else:
        user = User.query.filter_by(username = "guest").first()
        db.session.delete(user)
        db.session.commit()

# this functions are for form data
def make_dict(request):
    values = list(request.form.values())
    keys = list(request.form.keys())
    input = {}
    for i in range(len(keys)):
        value = values[i]
        key = keys[i]
        input.update({key:value})
    return input

def check_lens(targets):
    # The function is validating the length od inputs
    # Structure targets =
    # [{"target":string, "min_len":integer, "max_len":integer}, more dicts]
    # Returns True or a dict with Error and allowed max/ min length
    # If any len param is False the test for this param of the target will be
    # pased
    for i in range(len(targets)):
        # n is used because i is outranging the list
        n = i - 1
        if targets[n]["max_len"] == False:
            pass
        elif len(targets[n]["target"]) > targets[n]["max_len"]:
            error_report = {"target":targets[n]["target"], "error":1,
             "max_len":targets[n]["max_len"]}
            return error_report

        if targets[n]["min_len"] == False:
            pass
        elif len(targets[n]["target"]) < targets[n]["min_len"]:
            error_report = {"target":targets[n]["target"], "error":2,
            "min_len":targets[n]["min_len"]}
            return error_report

        else:
            pass
    return True

# Index is used for post search with the navbar forms and the profile search
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # Try to Say Welcome, if a user is alread logged in
        try:
            text = "Willkommen " + current_user.username + " auf der Website "
            return render_template("index.html", text=text)
        except:
            return render_template("index.html")

    if request.method == "POST":
        # Declare the search params for the post searchs with specific value
        type = "specific"
        spdict = ""
        return_url = request.referrer or "/"
        return search_results(request, type, spdict, return_url)

# The admin post variant is at this state not usable
@app.route("/admin/<method>/<username>", methods=["GET", "POST"])
@roles_required("Admin")
def admin(method, username):
    if request.method == "GET":
        if method == "edit":
            user = User.query.filter_by(username=username).first_or_404()
            return render_template("profile_specific_edit.html",
            user=user)

        return render_template("admin.html", method=method, username=username, \
        type="action")

# Shows last 5 Logins and will featuring in upcoming versions a load based
# Dashboard
@app.route("/admin", methods=["GET", "POST"])
@roles_required("Admin")
def admin_dashboard():
    login = logins.query.order_by("time_pr desc").limit(5).all()
    return render_template("admin.html", logins=login, type="view")

# Add User allows the Admin to add other Users with Roles
@app.route("/add-user", methods=["POST", "GET"])
@roles_required("Admin")
def add_user():
    if request.method == "GET":
        roles_all = Role.query.order_by(Role.name).all()
        return render_template("add_user.html", roles=roles_all)

    if request.method == "POST":
        # Get the list for roles
        multiselect = request.form.getlist("roles")

        # Check if username already exists
        if not User.query.filter_by(username=request.form["username"]).first():
            pass

        else:
            flash("Der Nutzername" +
            request.form["username"] + " ist schon vergeben")
            return redirect("/add-user")

        # Seting the targets for check_lens with lengths from config
        targets = [{"target":request.form["username"],
        "min_len":app.config["USER_USERNAME_MIN_LEN"],
        "max_len":app.config["USER_USERNAME_MAX_LEN"]},
        {"target":request.form["password"],
        "min_len":app.config["USER_PASSWORD_MIN_LEN"],
        "max_len":False},
        {"target":request.form["username"],
        "min_len":app.config["USER_USERNAME_MIN_LEN"],
        "max_len":app.config["USER_USERNAME_MAX_LEN"]},
        {"target":request.form["first_name"],
        "min_len":app.config["USER_FIRST_NAME_MIN_LEN"],
        "max_len":app.config["USER_FIRST_NAME_MAX_LEN"]},
        {"target":request.form["last_name"],
        "min_len":app.config["USER_LAST_NAME_MIN_LEN"],
        "max_len":app.config["USER_LAST_NAME_MAX_LEN"]}]
        check = check_lens(targets)

        # If everything is okay the user will be created
        if check == True:
            user = User(
            username = request.form["username"],
            password = user_manager.hash_password(request.form["password"]),
            first_name = request.form["first_name"],
            last_name = request.form["last_name"],
            )
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(username=request.form["username"]).first()
            for i in range(len(multiselect)):
                n = i - 1
                role = Role.query.filter_by(name=multiselect[n]).first()
                user_role = UserRoles(
                user_id = user.id,
                role_id = role.id
                )
                db.session.add(user_role)
                db.session.commit()
            flash("Der Nutzer " + request.form["username"] +
             " wurde erfolgreich hinzugefügt")
            return redirect("/add-user")
        # If sth is to short/ long return and flash with note for min/ max len
        else:
            if check["error"] == 1:
                flash(check["target"] + " ist zu lang (Maximal " +
                 str(check["max_len"]) + " Zeichen)")
                return redirect("/add-user")
            elif check["error"] == 2:
                flash(check["target"] + " ist zu kurz (Minimal " +
                str(check["min_len"]) + " Zeichen)")
                return redirect("/add-user")

# Not at this point usable
@app.route("/add-term", methods=["POST", "GET"])
@roles_required("Admin")
def add_term():
    if request.method == "GET":
        return render_template("add_term.html")

    if request.method == "POST":
        new_term = make_dict(request)
        return redirect("/add-term")

# Overview of al Log ins for tracing or overview
@app.route("/logins", methods=["GET", "POST"])
@roles_required("Admin")
def logins_view():
    if request.method == "GET":
        login = logins.query.order_by("time_pr desc").limit(100).all()
        return render_template("logins_overview.html", logins=login,
        current_page=1)

    if request.method == "POST":
        input = make_dict(request)
        login = logins.query.order_by("time_pr desc").limit(100).all()
        return logins_view_specific(input["page"])

# specific function for pages of logins
@app.route("/logins/<page>")
@roles_required("Admin")
def logins_view_specific(page):
    # Will take the page integer and make it to a number
    number = int(page) * 100 + 100
    login = logins.query.order_by("time_pr desc").limit(number).all()
    # Short the list by number
    login_list = login[:number]
    # If the page number is under 0 will be counted like page number is 0
    if int(page) < 0:
        login = logins.query.order_by("time_pr desc").limit(100).all()
        login_list = login[:100]
        return render_template("logins_overview.html", logins=login_list,
        current_page=0)
    return render_template("logins_overview.html", logins=login_list,
    current_page=int(page))

# The view functions for the results of the search
@app.route("/results")
@login_required
def search_results(request, type, spdict, return_url):
    if type == "specific":
        input = make_dict(request)

    elif type == "nonspecific":
        input = spdict

    else:
        flash("Error 02: Bad request")
        return redirect(return_url)
    len_s = ""

    if input["type"]=="broadcast":
        result_type = input["type"] or ""
        entrys.reindex()
        results = query, total = entrys.search(input["search"], 1, 100)
        if input["search"] == "":
                qry = db.session.query(entrys)
                results = qry.all()
                if len(entrys.query.all()) > 1:
                    text = " Es wurden " + str(len(entrys.query.all())) + \
                     " Ergebnisse gefunden:"
                else:
                    text = "Es wurde " + str(len(entrys.query.all())) + \
                     " Ergebnis gefunden: "
                if total == 0:
                    flash("Für diesen Suchbegriff wurde kein Ergebnis \
                     gefunden")
                    return redirect("/")
                return render_template("results.html", results=results,
                text=text, result_type=result_type)

    if input["type"]=="profile":
        User.reindex()
        result_type = input["type"]
        results = query, total = User.search(input["search"], 1 , 100)
        profile_results = []
        len_s = len(profile_results)
        for result in query:
            digest = hashlib.sha1(result.username.encode("utf-8")).hexdigest()
            avatar = "https://www.gravatar.com/avatar/{}?d=identicon&s=36".\
            format(digest)
            profile = {
            "username":result.username,
            "last_name":result.last_name,
            "first_name":result.first_name,
            "avatar_url":avatar
            }
            profile_results.append(profile)

        if input["search"] == "":
            results = db.session.query(User).order_by(User.username).all()
            len_s = len(results)
            profile_results = []
            if len(User.query.all()) > 1:
                    text = " Es wurden " + str(len(User.query.all())) + \
                     " Ergebnisse gefunden:"
            else:
                text = "Es wurde " + str(len(User.query.all())) + \
                 " Ergebnis gefunden: "

            for result in results:
                digest = hashlib.sha1(result.username.encode("utf-8")). \
                hexdigest()
                avatar = "https://www.gravatar.com/avatar/{}?d=identicon&s=36".\
                format(digest)
                profile = {
                "username":result.username,
                "last_name":result.last_name,
                "first_name":result.first_name,
                "avatar_url":avatar
                }
                profile_results.append(profile)

            return render_template("results.html", results=profile_results,
             text=text, result_type=result_type, len=len_s)


    if input["type"]=="term":
        terms.reindex()
        results = query, total = terms.search(input["search"], 1, 100)
        result_type = input["type"]
        if input["search"] == "":
                results = db.session.query(terms).all()
                if len(terms.query.all()) > 1:
                    text = " Es wurden " + str(len(terms.query.all())) + \
                     " Ergebnisse gefunden:"
                else:
                    text = "Es wurde " + str(len(terms.query.all())) + \
                     " Ergebnis gefunden: "
                if total == 0:
                    flash("Für diesen Suchbegriff wurde kein Ergebnis \
                     gefunden")
                    return redirect("/")
                return render_template("results.html", results=results,
                text=text, result_type=result_type)
        if total == 0:
            flash("Für diesen Suchbegriff wurde kein Ergebnis gefunden")
            return redirect("/")

    if results[1] > 1:
        text = "Es wurden " + str(total) + " Ergebnisse für den Suchbegriff " +\
         input["search"] + " gefunden:"

    elif results[1] == 1:
        text = "Es wurde 1 Ergebnis für den Suchbegriff " + input["search"] + \
         " gefunden:"

    elif not results:
        flash("Database Failure 01 - no FTS index or search data")
        return redirect(return_url)

    if result_type == "profile":
        length = len(profile_results)
        text = "Es wurde " + str(length) + " Ergebnis gefunden."
        if length > 1:
            text = "Es wurden " + str(length) + " Ergebnisse gefunden."
        return render_template("results.html", text=text, results = \
        profile_results, result_type=result_type, len=length)
    if total == 0:
        flash("Für diesen Suchbegriff wurde kein Ergebnis gefunden")
        return redirect("/")
    return render_template("results.html", results=results, text=text, \
    result_type=result_type, len=len_s)

# for custom info about owner/ hoster
# Currently Disabled but can enabled via config
if app.config["ABOUT_US"] == True:
    @app.route("/about-us")
    def about_us():
        return render_template(app.config["ABOUT_US_TEMPLATE"])

# Show user profile by username
@app.route("/profile/<username>")
@login_required
def profile_specific(username):
    user_searched = User.query.filter_by(username=username).first_or_404()
    current_user_level = current_user.level
    return render_template("profile_specific.html", user=user_searched, \
    logged_level=current_user_level )

# Profile base page
@app.route("/profile/")
def profile_redirect():
    return profile_main()

# For later implementation with hover user profile popups
@app.route("/profile/<username>/popup")
@login_required
def user_popup(username):
    user_searched = User.query.filter_by(username=username).first_or_404()
    return render_template("user_popup.html", user=user_searched)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile_main():
    if request.method == "GET":
        return render_template("profile_main.html")

    elif request.method == "POST":
        type = "specific"
        spdict = ""
        return_url = request.referrer or "/"
        return search_results(request, type, spdict, return_url)

# Makes an search for all terms/ entrys
@app.route("/all_terms")
@login_required
def all_terms():
    return_url = "/"
    spdict = {'search': '', 'type': 'term'}
    type = "nonspecific"
    return search_results("", type, spdict, return_url)

@app.route("/all_entrys")
@login_required
def all_entrys():
    return_url = "/"
    spdict = {'search': '', 'type': 'broadcast'}
    type = "nonspecific"
    return_url = request.referrer
    return search_results("", type, spdict, return_url)

# For later error report support
@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    if request.method == "GET":
        return render_template("report.html")

    if request.method == "POST":
        report = Reports(
        user = request.form["sender"],
        date = datetime.datetime.now(),
        error = request.form["error_code"],
        description = request.form["description"]
        )
        try:
            db.add(report)
            flash("Fehler gemeldet")
            return redirect("/")
        except:
            print("Fehler")
            return redirect("/")

# *Signals from flask user*

# Welcome flash message
@user_logged_in.connect_via(app)
def _after_login_hook(sender, user, **extra):
    flash(user.username + " logged in")
    return ""

# For recording of user logins if enabled
if app.config["TRACE_LOGIN"] == True:
    @user_logged_in.connect_via(app)
    def _track_logins(sender, user, **extra):
        # For geolocation suport watchout for python-geoip
        # This functions could be used for user analysis or multilanguage
        # support
        login = logins(
        ip = request.remote_addr,
        name = user.username,
        time = time.asctime(),
        time_pr = datetime.datetime.now()
        )
        db.session.add(login)
        db.session.commit()
        return ""

# Errorhandler pages

# Use 500 errorhandler for security, is ignored if debugging = True
@app.errorhandler(500)
def internal_server_error(e):
    er = "Serverfehler"
    return_url = request.referrer or "/"
    return render_template("error.html", return_url=return_url, error=er)

# For custom 403/ 404 page replace the error.html and remove unused Variables
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
