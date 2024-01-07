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
        prices = {"Wood": 800, "Marble": 1000, "Granite": 1500, "Bronze": 4500}
        return prices.get(self.stone_type, 0)

tombstones = [
    Tombstone("Wood", "In Loving Memory", 150, 70, 150),
    Tombstone("Marble", "In Loving Memory", 150, 70, 150),
    Tombstone("Granite", "In Loving Memory", 150, 70, 150),
    Tombstone("Bronze", "In Loving Memory", 150, 70, 150),
]