# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from recommendation import generate_diet_plan

app = FastAPI(title="HealthyMeal Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# EXPANDED DATABASE: 12 DISTINCT DISHES STRATIFIED BY TARGET PROFILES
MOCK_MEAL_DATABASE = [
    # --- LOW CALORIE DISHES (Matches targets below 900 Total Daily Calories) ---
    {"meal_id": 1, "name": "Clear Vegetable Broth Soup", "calories": 180, "tags": ["Vegetarian", "Low-Carb"], "allergens": [], "price": 6.50},
    {"meal_id": 2, "name": "Sautéed Tofu & Broccoli Steamer", "calories": 290, "tags": ["Vegetarian", "High-Protein"], "allergens": [], "price": 9.99},
    {"meal_id": 3, "name": "Lemon Herb Poached Whitefish", "calories": 260, "tags": ["Non-Vegetarian", "Low-Carb"], "allergens": [], "price": 13.25},
    {"meal_id": 4, "name": "Zucchini Noodles with Pesto", "calories": 220, "tags": ["Vegetarian", "Antioxidant-Rich"], "allergens": [], "price": 8.50},

    # --- MEDIUM CALORIE DISHES (Matches targets from 1000 - 1600 Total Daily Calories) ---
    {"meal_id": 5, "name": "Quinoa Avocado Salad Bowl", "calories": 450, "tags": ["Vegetarian", "Antioxidant-Rich"], "allergens": [], "price": 12.99},
    {"meal_id": 6, "name": "Spiced Paneer Protein Wrap", "calories": 500, "tags": ["Vegetarian", "High-Protein"], "allergens": ["Gluten"], "price": 11.00},
    {"meal_id": 7, "name": "Baked Salmon Salad with Spinach", "calories": 480, "tags": ["Non-Vegetarian", "High-Protein"], "allergens": [], "price": 16.50},
    {"meal_id": 8, "name": "Brown Rice and Lentil Dahl Bowl", "calories": 420, "tags": ["Vegetarian", "Complex-Carbs"], "allergens": [], "price": 9.25},

    # --- HIGH CALORIE DISHES (Matches targets above 1700 Total Daily Calories) ---
    {"meal_id": 9, "name": "Peanut Grilled Chicken Rice Bowl", "calories": 650, "tags": ["Non-Vegetarian", "High-Protein"], "allergens": ["Peanuts"], "price": 14.50},
    {"meal_id": 10, "name": "Creamy Chickpea Curry with Naan", "calories": 680, "tags": ["Vegetarian", "Complex-Carbs"], "allergens": ["Gluten"], "price": 11.95},
    {"meal_id": 11, "name": "Whole Wheat Mushroom Alfredo Pasta", "calories": 620, "tags": ["Vegetarian", "Complex-Carbs"], "allergens": ["Gluten"], "price": 12.50},
    {"meal_id": 12, "name": "Barbecue Chicken & Sweet Potato Mash", "calories": 710, "tags": ["Non-Vegetarian", "High-Protein"], "allergens": [], "price": 15.00}
]

class UserProfile(BaseModel):
    user_id: int
    name: str
    target_calories: int
    dietary_restriction: Optional[str] = None
    allergies: List[str] = []

@app.get("/")
def home():
    return {"message": "HealthyMeal System Backend is running!"}

@app.post("/api/recommendations")
def get_recommendations(profile: UserProfile):
    user_data = profile.dict()
    matched_meals = generate_diet_plan(user_data, MOCK_MEAL_DATABASE)
    if not matched_meals:
        raise HTTPException(status_code=404, detail="No dishes match your specific caloric brackets currently.")
    return {"user_name": profile.name, "recommended_meals": matched_meals}