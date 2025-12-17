# backend_fastapi/ai_engine.py

FOOD_MAP = {
    "normal": {
        "morning": ("Idli with Sambar", "Light, balanced start for energy"),
        "afternoon": ("Rice, Dal & Vegetables", "Balanced carbs and protein"),
        "evening": ("Fruit Bowl & Nuts", "Light snack for recovery"),
        "night": ("Vegetable Soup", "Easy to digest before sleep"),
    },
    "vegetarian": {
        "morning": ("Oats with Fruits", "High fiber and energy"),
        "afternoon": ("Veg Thali", "Complete vegetarian nutrition"),
        "evening": ("Paneer Sandwich", "Protein-rich snack"),
        "night": ("Salad & Soup", "Light and healthy dinner"),
    },
    "vegan": {
        "morning": ("Smoothie Bowl", "Plant-based energy"),
        "afternoon": ("Quinoa & Veggies", "High protein vegan meal"),
        "evening": ("Roasted Chickpeas", "Crunchy protein snack"),
        "night": ("Lentil Soup", "Warm and filling"),
    },
    "keto": {
        "morning": ("Egg Omelette", "Low-carb, high protein"),
        "afternoon": ("Grilled Paneer Bowl", "Keto-friendly fuel"),
        "evening": ("Cheese Cubes", "Fat-based energy"),
        "night": ("Veg Stir Fry", "Low-carb dinner"),
    },
    "paleo": {
        "morning": ("Fruit & Nuts", "Natural energy"),
        "afternoon": ("Grilled Veg Bowl", "Clean eating"),
        "evening": ("Boiled Eggs", "Protein boost"),
        "night": ("Clear Soup", "Light paleo meal"),
    },
    "diabetic": {
        "morning": ("Multigrain Toast", "Low GI food"),
        "afternoon": ("Brown Rice & Veg", "Controlled carbs"),
        "evening": ("Sprouts Salad", "Fiber rich"),
        "night": ("Veg Soup", "Blood sugar friendly"),
    },
    "high_protein": {
        "morning": ("Protein Smoothie", "Muscle fuel"),
        "afternoon": ("Protein Bowl", "Sustained energy"),
        "evening": ("Boiled Eggs", "Quick protein"),
        "night": ("Paneer Stir Fry", "Recovery meal"),
    },
}

def get_meal_recommendation(diet: str, time_of_day: str):
    diet = diet.lower()
    time_of_day = time_of_day.lower()

    meal, reason = FOOD_MAP.get(
        diet,
        FOOD_MAP["normal"]
    ).get(
        time_of_day,
        ("Healthy Meal", "Balanced nutrition")
    )

    return {
        "meal": meal,
        "reason": reason
    }
