import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hydration.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show landing page"""
    return render_template("index.html")


@app.route('/', methods=['POST'])
def result():
    # Water intake calculator (formula derrived from https://www.healthline.com/nutrition/7-health-benefits-of-water)
    weight = request.form.get("weight", type=int, default=0)
    hours = request.form.get("hours", type=int, default=0)
    climate = request.form.get("climate")
    if(climate == 'Yes'):
        result = ((1/3) * weight) + ((24) * hours) + 16
    elif(climate == 'No'):
        result = ((1/3) * weight) + ((24) * hours)
    else:
        result = 0
    entry1 = int(result)
    entry2 = round(int(result) / 8)
    return render_template('index.html', entry1=entry1, entry2=entry2)


@app.route("/log")
@login_required
def wlog():
    """Show log of water_log"""

    # Gets all the info from the purchase table for that user
    water_table = db.execute("SELECT * FROM water_log WHERE user_id = ?", session["user_id"])
    total_ounces = db.execute(
        "SELECT SUM(ounces) AS ounces FROM water_log WHERE user_id = ?", session["user_id"])[0]["ounces"]

    if total_ounces == 0:
        total_ounces = 0

    # Displays that water log table on the log.html file
    return render_template("log.html", water_log=water_table, total=total_ounces)


@app.route("/nlog", methods=["POST", "GET"])
@login_required
def add_ounces():
    """Allows user to add new water logs"""

    if request.method == "POST":
        # Checks if an amount was inputted
        if not request.form.get("ounces"):
            return apology("Please insert how many ounces you want to add", 400)

        # Adds ounces into user database so they know how much water they drank
        db.execute("INSERT INTO water_log (user_id, ounces) VALUES (?, ?)",
                    session["user_id"], (request.form.get("ounces")))

        return redirect("/log")
    else:
        return render_template("nlog.html")


@app.route("/log", methods=["POST", "GET"])
@login_required
def new_day():
    """Allow user to log a new days worth of water"""

    if request.method == "POST":

        # Updates the amount of money the user has to spend
        db.execute("DELETE FROM water_log WHERE user_id = ?",
                    session["user_id"])

        return redirect("/log")
    else:
        return render_template("log.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash_pw"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Checks if a username was inputted
        if not request.form.get("username"):
            return apology("Username is required", 400)

        # Checks if a password was inputted
        elif not request.form.get("password"):
            return apology("Password is required", 400)

        # Checks if a confirmation was inputted
        elif not request.form.get("confirmation"):
            return apology("Please confirm your password", 400)

        # Checks if the password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords must match")

        # Inserts username/password combo into the user database if username isn't already taken (Thanks to section for teaching try function)
        try:
            db.execute("INSERT INTO users (username, hash_pw) VALUES (?, ?)",
                       request.form.get("username"), generate_password_hash(request.form.get("password")))
        except:
            return apology("Username is taken", 400)

        return redirect("/")

    else:
        return render_template("register.html")