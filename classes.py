# Define classes for Casket, Tombstone, and Urn
class Casket:
    def __init__(self, wood_type, length, width, depth):
        self.wood_type = wood_type
        self.length = length
        self.width = width
        self.depth = depth


class Tombstone:
    def __init__(self, stone_type, engraving, length, width):
        self.stone_type = stone_type
        self.engraving = engraving
        self.length = length
        self.width = width


class Urn:
    def __init__(self, volume, color):
        self.volume = volume
        self.color = color


# User class for registration and login
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


# Sample user data (you can replace this with a database)
users = [User("john_doe", "password123"), User("jane_smith", "pass456")]
# users = [...]


# Sample data (you can replace this with a database)
caskets = [Casket("Oak", 200, 80, 60), Casket("Mahogany", 210, 85, 65)]
# caskets = [...]

tombstones = [
    Tombstone("Marble", "In Loving Memory", 150, 70),
    Tombstone("Granite", "Forever Remembered", 160, 75),
]
# tombstones = [...]

urns = [Urn(5, "White"), Urn(3, "Black")]
# urns = [...]
