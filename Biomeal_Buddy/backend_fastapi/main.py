from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="Biomeal Buddy API")

# ---------------- MODELS ---------------- #

class MealRequest(BaseModel):
    sleep_hours: int
    steps: int
    heart_rate: int
    diet: str
    time_of_day: str

class RestaurantRequest(BaseModel):
    diet: str

# ---------------- MEAL ENGINE ---------------- #

@app.post("/recommend")
def recommend_meal(req: MealRequest):

    meals = {
        "vegetarian": ["Vegetable Upma", "Paneer Salad", "Veg Khichdi"],
        "vegan": ["Oats Bowl", "Fruit Smoothie", "Vegan Stir Fry"],
        "keto": ["Avocado Egg Bowl", "Grilled Chicken", "Paneer Keto Bowl"],
        "paleo": ["Grilled Fish", "Chicken Veg Bowl"],
        "diabetic": ["Millet Roti & Sabzi", "Low GI Salad"],
        "high_protein": ["Egg Whites & Toast", "Protein Bowl"],
        "normal": ["Idli Sambar", "Rice & Dal"]
    }

    meal = random.choice(meals.get(req.diet, meals["normal"]))

    return {
        "meal": meal,
        "reason": "Selected based on your activity, heart rate and diet preference."
    }

# ---------------- RESTAURANT ENGINE ---------------- #

@app.post("/restaurants")
def get_restaurants(req: RestaurantRequest):

    all_restaurants = [
        {"name": "Green Leaf Kitchen", "diet": ["vegetarian", "vegan"], "rating": 4.6, "distance": 1.2, "time": 15},
        {"name": "Keto Fuel Cafe", "diet": ["keto"], "rating": 4.7, "distance": 2.8, "time": 22},
        {"name": "Healthy Bites", "diet": ["diabetic", "normal"], "rating": 4.4, "distance": 1.9, "time": 18},
        {"name": "Protein Hub", "diet": ["high_protein"], "rating": 4.8, "distance": 3.0, "time": 25},
        {"name": "Pure Veg Delight", "diet": ["vegetarian"], "rating": 4.3, "distance": 1.5, "time": 16},
    ]

    filtered = [r for r in all_restaurants if req.diet in r["diet"]]

    # Sort by distance (nearest first)
    filtered.sort(key=lambda x: x["distance"])

    return filtered
