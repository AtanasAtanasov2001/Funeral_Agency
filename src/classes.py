
# Define classes for Casket, Tombstone, and Urn
class Casket:
    def __init__(self, wood_type, length, width, depth):
        self.wood_type = wood_type
        self.length = length
        self.width = width
        self.depth = depth

    def display(self):
        return f"Casket - Wood Type: {self.wood_type}, Length: {self.length}, Width: {self.width}, Depth: {self.depth}"
    
    def calculate_price(self):
        # Implement casket pricing logic
        prices = {"Oak": 500, "Mahogany": 600, "Pine": 650, "Walnut": 1000}
        return prices.get(self.wood_type, 0)


caskets = [Casket("Oak", 215, 80, 60), Casket("Mahogany", 215, 80, 60), Casket("Pine", 215, 80, 60), Casket("Walnut", 215, 80, 60)]
# caskets = [...]

class Tombstone:
    def __init__(self, stone_type, engraving, length, width, height):
        self.stone_type = stone_type
        self.engraving = engraving
        self.length = length
        self.width = width
        self.height = height
        
    def display(self):
        return f"Tombstone - Stone Type: {self.stone_type}, Engraving: {self.engraving}, Length: {self.length}, Width: {self.width}, Height: {self.height}"

    def calculate_price(self):
        # Implement tombstone pricing logic
        prices = {"Wood": 800, "Marble": 1000, "Granite": 1500, "Bronze": 4500}
        return prices.get(self.stone_type, 0)

tombstones = [
    Tombstone("Wood", "In Loving Memory", 150, 70, 150),
    Tombstone("Marble", "In Loving Memory", 150, 70, 150),
    Tombstone("Granite", "In Loving Memory", 150, 70, 150),
    Tombstone("Bronze", "In Loving Memory", 150, 70, 150),
]
# tombstones = [...]

class Urn:
    def __init__(self, volume, material, color):
        self.volume = volume
        self.material = material
        self.color = color
        
    def display(self):
        color_display = self.color.capitalize() if self.color is not None else "N/A"
        return f"Urn - Volume: {self.volume}, Material: {self.material}, Color: {color_display}"
    
    def calculate_price(self):
        # Check if any of the attributes is None
        if self.volume is None or self.material is None or self.color is None:
            return 0
        
        # Implement urn pricing logic
        prices = {"Plastic": 100, "Metal": 200, "Ceramic": 500}
        return prices.get(self.material, 0)

urns = [Urn(250, "Plastic", "Black"), Urn(250, "Metal", "Black"), Urn(250, "Ceramic", "Black")]

# urns = [...]

# User class for registration and login
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Sample user data (you can replace this with a database)
users = [User("john_doe", "password123"), User("jane_smith", "pass456")]
# users = [...]


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
                total_price += item.calculate_price()
            elif isinstance(item, Tombstone):
                total_price += item.calculate_price()
            elif isinstance(item, Urn):
                total_price += item.calculate_price()
        return total_price
    
# Cart instance
cart = Cart()
