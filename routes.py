from app import app

@app.route("/", methods=["POST", "GET"])
def index():
    if method == "GET":
        return render_template("index.html")

    if method == "Post":
        # add search answer with search mixin
