from flask import Flask, render_template, redirect, request, session, flash
import re
import datetime
DIG_REGEX = re.compile(r".*[0-9].*")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
UPPER_REGEX = re.compile(r".*[A-Z].*")
app = Flask(__name__)
app.secret_key = "KeepItSecretKeepItSafe"
@app.route("/")
def form():
    return render_template("index.html")
@app.route("/reg", methods=["POST"])
def valid():
    valid = True
    if len(request.form["first_name"]) < 1:
        flash("First name must not be blank!")
        valid = False
    elif DIG_REGEX.match(request.form["first_name"]):
        flash("First name cannot contain numbers!")
        valid = False
    if len(request.form["last_name"]) < 1:
        flash("Last name must not be blank!")
        valid = False
    elif DIG_REGEX.match(request.form["last_name"]):
        flash("Last name cannot contain numbers!")
        valid = False
    if len(request.form["birth_date"]) <1:
        flash("Birthdate must not be blank!")
        valid = False
    else:
        print request.form["birth_date"]
        try:
            birth_date = datetime.datetime.strptime(request.form["birth_date"], "%Y-%m-%d").date()
            if birth_date > datetime.date.today():
                flash("Birthdate cannot be in the future!")
                valid = False
        except ValueError:
            flash("Invalid date!")
            valid = False
    if len(request.form["email"]) < 1:
        flash("Email must not be blank!")
        valid = False
    elif not EMAIL_REGEX.match(request.form["email"]):
        flash("Invalid email!")
        valid = False
    if len(request.form["password"]) < 1:
        flash("Password must not be blank!")
        valid = False
    elif len(request.form["password"])<8:
        flash("Password must be 8 or more characters!")
        valid = False
    else:
        if not UPPER_REGEX.match(request.form["password"]):
            flash("Password must have at least 1 uppercase letter!")
            valid = False
        if not DIG_REGEX.match(request.form["password"]):
            flash("Password must have at least 1 number!")
            valid = False
    if len(request.form["confirm_password"]) < 1:
        flash("Password confirmation cannot be blank!")
        valid = False
    elif request.form["password"] != request.form["confirm_password"]:
        flash("Password confirmation must match password!")
        valid = False
    if valid:
        flash("Thanks for submitting your information.")
    return redirect("/")
app.run(debug=True)