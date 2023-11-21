# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import users, User, caskets, tombstones, urns

main_blueprint = Blueprint("main", __name__)


def home():
    username = session.get("username")
    return render_template(
        "home.html",
        caskets=caskets,
        tombstones=tombstones,
        urns=urns,
        username=username,
    )


main_blueprint.route("/", methods=["GET"])(home)


def pay():
    # Extract payment details from the form
    card_num = request.form.get("card_num")
    cardholder_name = request.form.get("cardholder_name")
    valid_until = request.form.get("valid_until")
    ccv = request.form.get("ccv")

    # Process the payment (you can add your logic here)

    return render_template("payment.html")


main_blueprint.route("/pay", methods=["POST"])(pay)


def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the username is already taken
        if any(user.username == username for user in users):
            return render_template("register.html", error="Username already taken")

        # Add the new user to the list (in-memory storage, replace with a database)
        users.append(User(username, password))

        # Redirect to the login page after successful registration
        return redirect(url_for("main.login"))

    return render_template("register.html")


main_blueprint.route("/register", methods=["GET", "POST"])(register)


def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the provided credentials are valid
        user = next(
            (
                user
                for user in users
                if user.username == username and user.password == password
            ),
            None,
        )

        if user:
            session["username"] = username  # Store the username in the session
            return redirect(url_for("main.home"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


main_blueprint.route("/login", methods=["GET", "POST"])(login)


def logout():
    session.pop("username", None)
    return redirect(url_for("main.home"))


main_blueprint.route("/logout")(logout)


# from app import app
