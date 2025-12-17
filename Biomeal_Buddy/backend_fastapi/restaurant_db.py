# backend_fastapi/restaurant_db.py

RESTAURANTS = {
    "normal": [
        {"name": "Home Spice Kitchen", "time": "15 mins", "price": "₹120–180"},
        {"name": "Urban Tiffins", "time": "20 mins", "price": "₹150–220"}
    ],

    "vegetarian": [
        {"name": "Green Leaf Veg", "time": "15 mins", "price": "₹130–200"},
        {"name": "Pure Veg Bowl", "time": "18 mins", "price": "₹140–210"}
    ],

    "vegan": [
        {"name": "Vegan Vibes", "time": "20 mins", "price": "₹180–250"},
        {"name": "Plant Power Cafe", "time": "25 mins", "price": "₹200–280"}
    ],

    "keto": [
        {"name": "Keto Kitchen", "time": "20 mins", "price": "₹250–350"},
        {"name": "Low Carb Hub", "time": "22 mins", "price": "₹270–360"}
    ],

    "paleo": [
        {"name": "Nature Grill", "time": "25 mins", "price": "₹300–400"},
        {"name": "Tribal Foods", "time": "30 mins", "price": "₹320–420"}
    ],

    "diabetic": [
        {"name": "Healthy Bites", "time": "18 mins", "price": "₹200–260"},
        {"name": "SugarSmart Kitchen", "time": "20 mins", "price": "₹220–280"}
    ],

    "high_protein": [
        {"name": "Protein Hub", "time": "20 mins", "price": "₹280–380"},
        {"name": "Fit Fuel Cafe", "time": "22 mins", "price": "₹300–420"}
    ]
}
