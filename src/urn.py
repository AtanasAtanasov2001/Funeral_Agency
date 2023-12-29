
class Urn:
    def __init__(self, volume, material, color):
        self.volume = volume
        self.material = material
        self.color = color
        
    def display(self):
        color_display = self.color.capitalize() if self.color is not None else "N/A"
        return f"Urn - Material: {self.material}, Volume: {self.volume}, Color: {color_display}"
    
    def calculate_price(self):
        # Check if any of the attributes is None
        if self.volume is None or self.material is None or self.color is None:
            return 0
        
        # Implement urn pricing logic
        prices = {"Plastic": 100, "Metal": 200, "Ceramic": 500}
        return prices.get(self.material, 0)

urns = [Urn(250, "Plastic", "Black"), Urn(250, "Metal", "Black"), Urn(250, "Ceramic", "Black")]