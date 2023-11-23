# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from src.classes import users, User, caskets, tombstones, urns, cart

main_blueprint = Blueprint("main", __name__)

from app import app

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


def add_to_cart():
    item_type = request.form.get("item_type")
    if item_type == "casket":
        item = Casket(
            wood_type=request.form.get("wood_type"),
            length=int(request.form.get("length")),
            width=int(request.form.get("width")),
            depth=int(request.form.get("depth")),
        )
    elif item_type == "tombstone":
        item = Tombstone(
            stone_type=request.form.get("stone_type"),
            engraving=request.form.get("engraving"),
            length=int(request.form.get("length")),
            width=int(request.form.get("width")),
        )
    elif item_type == "urn":
        item = Urn(
            material=request.form.get("material"),
            volume=int(request.form.get("volume")),
            color=request.form.get("color"),
        )
    else:
        return redirect(url_for("main.home"))

    # Add the selected item to the cart
    cart.add_item(item)

    return redirect(url_for("main.home"))

main_blueprint.route("/add_to_cart", methods=["POST"])(add_to_cart)


def choose_burial_type():
    if request.method == "POST":
        burial_type = request.form.get("burial_type")
        session["burial_type"] = burial_type
        return redirect(url_for("main.customize", burial_type=burial_type))

    return render_template("choose_burial_type.html")

main_blueprint.route("/choose_burial_type", methods=["GET", "POST"])(choose_burial_type)

def customize(burial_type):
    # Ensure a valid burial type is selected
    if burial_type not in ["Cremation", "Ordinary"]:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        # Handle customization options for POST requests
        if burial_type == "Ordinary":
            # Handle customization options for Ordinary Burial (caskets and tombstones)
            wood_type = request.form.get("wood_type")
            length = int(request.form.get("length"))
            width = int(request.form.get("width"))
            depth = int(request.form.get("depth"))

            # Add the customized casket to the cart (you can replace this with your logic)
            casket = Casket(wood_type, length, width, depth)
            # Add the casket to the cart or perform other actions as needed
            # ...

        elif burial_type == "Cremation":
            # Handle customization options for Cremation (urns)
            volume = int(request.form.get("volume"))
            kind = request.form.get("kind")

            # Add the customized urn to the cart (you can replace this with your logic)
            urn = Urn(volume, kind)
            # Add the urn to the cart or perform other actions as needed
            # ...

    # Render the customization page with burial type information for GET requests
    if request.method == "GET":
        return render_template("customize.html", burial_type=burial_type, caskets=caskets, tombstones=tombstones, urns=urns)

    # Redirect to the home page or another appropriate page after handling the customization
    return redirect(url_for("main.home"))

main_blueprint.route("/customize/<burial_type>", methods=["GET", "POST"])(customize)


def cart():
    # Add logic to retrieve items from the cart
    # ...

    return render_template("cart.html", burial_type=session.get("burial_type"))

main_blueprint.route("/cart", methods=["GET"])(cart)


def payment():
    if request.method == "POST":
        # Calculate the total price
        total_price = cart.calculate_price()
        return render_template("payment.html", total_price=total_price)
    return render_template("payment.html")

main_blueprint.route("/payment", methods=["GET", "POST"])(payment)