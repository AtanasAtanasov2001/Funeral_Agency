# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.classes import users, User, Casket, Tombstone, Urn, Cart, caskets, tombstones, urns, cart

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


def parse_display_string(display_string):
    # Split the display string into parts
    parts = display_string.split(', ')

    # Create a dictionary to store key-value pairs
    item_info = {}

    # Extract the item type from the first part
    item_type, rest_of_string = parts[0].split(' - ')
    item_info["Item Type"] = item_type.strip()

    # Process the rest of the string
    for part in rest_of_string.split(', '):
        key, value = part.split(': ')
        item_info[key.strip()] = value.strip()

    # Determine the item type and create the corresponding object
    if item_info["Item Type"] == "Urn":
        return Urn(
            volume=int(item_info.get("Volume", 0)),
            material=item_info.get("Material", ""),
            color=item_info.get("Color", "")
        )
    elif item_info["Item Type"] == "Casket":
        return Casket(
            wood_type=item_info.get("Wood Type", ""),
            length=int(item_info.get("Length", 0)),
            width=int(item_info.get("Width", 0)),
            depth=int(item_info.get("Depth", 0))
        )
    elif item_info["Item Type"] == "Tombstone":
        return Tombstone(
            stone_type=item_info.get("Stone Type", ""),
            engraving=item_info.get("Engraving", ""),
            length=int(item_info.get("Length", 0)),
            width=int(item_info.get("Width", 0)),
            height=int(item_info.get("Height", 0))
        )
    # Add more conditions for other item types

    # If no condition matches, return None or raise an error
    return None


def add_to_cart():
    print("ENTER ADD_TO_CART")
    item_type = request.form.get("item_type")
    burial_type = request.form.get("burial_type")
    print("Item Type:", item_type)
    print("Burial Type:", burial_type)
    
    item = parse_display_string(item_type)

    # Add the selected item to the cart
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
        # Handle other cases or raise an error
        return redirect(url_for("main.default_contents/<burial_type>"))
    
main_blueprint.route("/default_contents/<burial_type>", methods=["GET"])(default_contents)
    

def customize(burial_type):
    print("Entered Customize Endpoint")
    print(f"Burial Type: {burial_type}")

    # Ensure a valid burial type is selected
    if burial_type.lower() not in ["cremation", "ordinary"]:
        print("Invalid Burial Type, Redirecting to Home")
        return redirect(url_for("main.home"))

    # Retrieve existing options for caskets, tombstones, and urns
    existing_caskets = [casket.wood_type for casket in caskets]
    existing_tombstones = [tombstone.stone_type for tombstone in tombstones]
    existing_urns = [urn.material for urn in urns]

    # Add the existing options to the context for rendering in the template
    context = {
        'burial_type': burial_type,
        'existing_caskets': existing_caskets,
        'existing_tombstones': existing_tombstones,
        'existing_urns': existing_urns,
    }
    
    # print("Existing Caskets:", existing_caskets)
    # print("Existing Tombstones:", existing_tombstones)
    # print("Existing Urns:", existing_urns)

    if request.method == "POST":
        # Handle customization options for POST requests
        print("Handling POST request")
        print(request.form)  # Print the form data for debugging

        # Handle customization options for POST requests
        if burial_type == "ordinary":
            # Handle customization options for Ordinary Burial (caskets and tombstones)
            wood_type = request.form.get("wood_type")
            length = int(request.form.get("length"))
            width = int(request.form.get("width"))
            depth = int(request.form.get("depth"))

            # Add the customized casket to the cart
            new_casket = Casket(wood_type, length, width, depth)
            caskets.append(new_casket)
            cart.add_item(new_casket)


            # Handle customization options for Tombstone
            stone_type = request.form.get("stone_type")
            engraving = request.form.get("engraving")
            length_tombstone = int(request.form.get("tombstone_length"))
            width_tombstone = int(request.form.get("tombstone_width"))
            height_tombstone = int(request.form.get("tombstone_height"))

            # Add the customized tombstone to the cart
            new_tombstone = Tombstone(stone_type, engraving, length_tombstone, width_tombstone, height_tombstone)
            tombstones.append(new_tombstone)
            cart.add_item(new_tombstone)


        elif burial_type == "cremation":
            # Handle customization options for Cremation (urns)
            volume = int(request.form.get("volume"))
            kind = request.form.get("kind")
            color = request.form.get("color")

            # Add the customized urn to the cart
            new_urn = Urn(volume, kind, color)
            urns.append(new_urn)
            cart.add_item(new_urn)

        session.setdefault("_flashes", []).append(("success", "Customization data saved successfully"))

        # Redirect to the customization page with the burial type
        return redirect(url_for("main.customize", burial_type=burial_type))


    # Render the customization page with burial type information and existing options
    return render_template("customize.html", **context)



main_blueprint.route("/customize/<burial_type>", methods=["GET", "POST"])(customize)


def cart_contents():
    global cart
    
    
    # Calculate the total price
    total_price = cart.calculate_price()
    # Access the Cart instance from your module
    print("Cart Items:", cart.items)
    print("Total Price:", total_price)


    # Render the cart page with items and total price
    return render_template("cart.html", items=cart.items, total_price=total_price)

main_blueprint.route("/cart", methods=["GET"])(cart_contents)


def payment():
    if request.method == "POST":
        # Calculate the total price
        total_price = cart.calculate_price()
        return render_template("payment.html", total_price=total_price)
    return render_template("payment.html")

main_blueprint.route("/payment", methods=["GET", "POST"])(payment)