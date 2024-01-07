# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.casket import  Casket, caskets
from src.cart import Cart, cart
from src.tombstone import  Tombstone, tombstones
from src.user import users, User
from src.urn import Urn, urns

import re
from datetime import datetime

main_blueprint = Blueprint("main", __name__)


def home():
    username = session.get("username")
    burial_type = session.get("burial_type") 
    return render_template(
        "home.html",
        caskets=caskets,
        tombstones=tombstones,
        urns=urns,
        username=username,
        burial_type=burial_type
    )

main_blueprint.route("/", methods=["GET"])(home)


def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the username is already taken
        if any(user.username == username for user in users):
            return render_template("register.html", error="Username already taken")

        # Create a new user and add it to the list
        new_user = User(username, password)
        users.append(new_user)

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


def convert_to_numeric(value):
    try:
        return int(value)
    except ValueError:
        print(f"Failed to convert value to an integer: {value}")
        return 0

def parse_display_string(display_string):
    print(f"Original display_string: {display_string}")

    # Split the display string into parts
    parts = display_string.split(' - ', 1)

    # Create a dictionary to store key-value pairs
    item_info = {"Item Type": parts[0].strip()}

    print(f"Item Type: {item_info['Item Type']}")
    print(f"Rest of String: {parts[1]}")

    # Process the rest of the string
    for part in parts[1].split(', '):
        key, value = part.split(': ')
        key_lower = key.strip().lower()
        value_stripped = value.strip()

        print(f"Key: {key_lower}, Value: {value_stripped}")

        
        if key_lower in ["length", "width", "depth", "height", "volume"]:
            item_info[key_lower] = convert_to_numeric(value_stripped)
        else:
            item_info[key_lower] = value_stripped

    print(f"Parsed Item Info: {item_info}")

    if item_info["Item Type"] == "Urn":
        return Urn(
            material=item_info.get("material", ""),
            volume=item_info.get("volume", 0),
            color=item_info.get("color", "")
        )
    elif item_info["Item Type"] == "Casket":
        return Casket(
            wood_type=item_info.get("wood type", ""),
            length=item_info.get("length", 0),
            width=item_info.get("width", 0),
            depth=item_info.get("depth", 0),
        )
    elif item_info["Item Type"] == "Tombstone":
        return Tombstone(
            stone_type=item_info.get("stone type", ""),
            engraving=item_info.get("engraving", ""),
            length=item_info.get("length", 0),
            width=item_info.get("width", 0),
            height=item_info.get("height", 0),
        )

    return None




def add_to_cart():
    print("ENTER ADD_TO_CART")
    display_string = request.form.get('item_type_dropdown')
    burial_type = request.form.get('burial_type')
    customize = request.form.get('customize')
    print("Item Type:", display_string)
    print("Burial Type:", burial_type)
    print("Customize:", customize )
    
    if customize == 'True':
        print("ENTER")
        if burial_type == "ordinary":
            print("ENTER ordinary")
            wood_type = request.form.get("wood_type")
            length = int(request.form['casket_length'])
            width = int(request.form['casket_width'])
            depth = int(request.form['casket_depth'])

            if length < 60 or width < 60 or depth < 60:
                raise ValueError("The length/width/depth must be a valid number")

            new_casket = Casket(wood_type, length, width, depth)
            caskets.append(new_casket)
            cart.add_item(new_casket)

            stone_type = request.form['stone_type']
            engraving = request.form['engraving']
            length_tombstone = int(request.form['tombstone_length'])
            width_tombstone = int(request.form['tombstone_width'])
            height_tombstone = int(request.form['tombstone_height'])

            if length_tombstone < 60 or width_tombstone < 60 or height_tombstone < 60:
                raise ValueError("The length/width/height must be positive number")
            

            new_tombstone = Tombstone(stone_type, engraving, length_tombstone, width_tombstone, height_tombstone)
            tombstones.append(new_tombstone)
            cart.add_item(new_tombstone)


        elif burial_type == "cremation":
            print("ENTER cremation")


            volume = int(request.form['volume'])
            if volume < 100:
                raise ValueError("The volume must be positive number")
            
            kind = request.form.get('material')
            color = request.form.get('color')


            new_urn = Urn(volume, kind, color)
            urns.append(new_urn)
            cart.add_item(new_urn)

        session.setdefault("_flashes", []).append(("success", "Customization data saved successfully"))


        return redirect(url_for("main.cart_contents"))

    else:
        item = parse_display_string(display_string)
        print("Parsed item:", item)
        cart.add_item(item)

    return redirect(url_for("main.cart_contents"))

main_blueprint.route("/add_to_cart", methods=["POST"])(add_to_cart)

def default_contents(burial_type):
    default_caskets = caskets
    default_tombstones = tombstones
    default_urns = urns
    
    if burial_type == "ordinary":
        return render_template("default_contents.html", default_choices=default_caskets + default_tombstones, item_type="Item", burial_type=burial_type)
    elif burial_type == "cremation":
        return render_template("default_contents.html", default_choices=default_urns, item_type="Urn", burial_type=burial_type)
    else:
        flash("Invalid burial type")  # Optional: Provide a user-friendly message
        return redirect(url_for("home.html")) 
    
main_blueprint.route("/default_contents/<burial_type>", methods=["GET"])(default_contents)
    

def customize(burial_type):
    if burial_type.lower() not in ["cremation", "ordinary"]:
        print("Invalid Burial Type, Redirecting to Home")
        return redirect(url_for("main.home"))

    existing_caskets = [casket.wood_type for casket in caskets]
    existing_tombstones = [tombstone.stone_type for tombstone in tombstones]
    existing_urns = [urn.material for urn in urns]

    context = {
        'burial_type': burial_type,
        'existing_caskets': existing_caskets,
        'existing_tombstones': existing_tombstones,
        'existing_urns': existing_urns,
    }

    return render_template("customize.html", **context)



main_blueprint.route("/customize/<burial_type>", methods=["GET", "POST"])(customize)


def cart_contents():
    global cart
    
    
    total_price = cart.calculate_price()

    return render_template("cart.html", items=cart.items, total_price=total_price)

main_blueprint.route("/cart", methods=["GET"])(cart_contents)


def is_valid_card_type(card_type):
    return card_type in ["Visa","MasterCard", "Maestro"]

def is_valid_card_number(card_number):
    # Check if the card number is 16 digits
    return re.match(r'^\d{16}$', card_number) is not None

def is_valid_expiration_date(expiration_date):
    try:
        # Check if the expiration date is a valid date and not expired
        expiration_date = datetime.strptime(expiration_date, '%m/%Y')
        return expiration_date > datetime.now()
    except ValueError:
        return False

def is_valid_cvv(cvv):
    # Check if the CVV is 3 digits
    return re.match(r'^\d{3}$', cvv) is not None

def is_valid_cardholder_name(cardholder_name):
    # Check if the cardholder name is a valid string
    return bool(cardholder_name.strip())

def payment():
    if request.method == "POST":
        card_type = request.form['card_type']
        card_number = request.form['card_number']
        expiration_date = request.form['expiration_date']
        cvv = request.form['cvv']
        cardholder_name = request.form['cardholder_name']

        if (
            is_valid_card_type(card_type) and 
            is_valid_card_number(card_number) and
            is_valid_expiration_date(expiration_date) and
            is_valid_cvv(cvv) and
            is_valid_cardholder_name(cardholder_name)
        ):
            total_price = cart.calculate_price()
            cart.items = []
            flash("Valid payment, redirecting to home menu.")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid payment details. Please check your information and try again.", "error")

    # Render the payment form
    return render_template("payment.html")

main_blueprint.route("/payment", methods=["GET", "POST"])(payment)
