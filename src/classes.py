# Define classes for Casket, Tombstone, and Urn
class Casket:
    def __init__(self, wood_type, length, width, depth):
        self.wood_type = wood_type
        self.length = length
        self.width = width
        self.depth = depth


caskets = [Casket("Oak", 215, 80, 60), Casket("Mahogany", 215, 80, 60), Casket("Pine", 215, 80, 60), Casket("Walnut", 215, 80, 60)]
# caskets = [...]

class Tombstone:
    def __init__(self, stone_type, engraving, length, width, height):
        self.stone_type = stone_type
        self.engraving = engraving
        self.length = length
        self.width = width
        self.height = height


tombstones = [
    Tombstone("Wood", "In Loving Memory", 150, 70, 150),
    Tombstone("Marble", "In Loving Memory", 150, 70, 150),
    Tombstone("Granite", "In Loving Memory", 150, 70, 150),
    Tombstone("Bronze", "In Loving Memory", 150, 70, 150),
]
# tombstones = [...]

class Urn:
    def __init__(self, volume, kind):
        self.volume = volume
        self.kind = kind

urns = [Urn(250, "Plastic"), Urn(250, "Metal"), Urn(250, "Ceramic")]
# urns = [...]

# User class for registration and login
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Sample user data (you can replace this with a database)
users = [User("john_doe", "password123"), User("jane_smith", "pass456")]
# users = [...]


# Cart class to store selected items
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def calculate_price(self):
        # Implement pricing logic based on the selected items
        total_price = 0
        for item in self.items:
            if isinstance(item, Casket):
                total_price += calculate_casket_price(item)
            elif isinstance(item, Tombstone):
                total_price += calculate_tombstone_price(item)
            elif isinstance(item, Urn):
                total_price += calculate_urn_price(item)
        return total_price

def calculate_casket_price(casket):
    # Implement casket pricing logic
    prices = {"Oak": 500, "Mahogany": 600, "Pine": 650, "Walnut": 1000}
    return prices.get(casket.wood_type, 0)

def calculate_tombstone_price(tombstone):
    # Implement tombstone pricing logic
    prices = {"Wood": 800, "Marble": 1000, "Granite": 1500, "Bronze": 4500}
    return prices.get(tombstone.stone_type, 0)

def calculate_urn_price(urn):
    # Implement urn pricing logic
    prices = {"Plastic": 100, "Metal": 200, "Ceramic": 500}
    return prices.get(urn.material, 0)


# Cart instance
cart = Cart()
