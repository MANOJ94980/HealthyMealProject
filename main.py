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
# Updated database in main.py with exact macro gram values per serving
MOCK_MEAL_DATABASE = [
    # --- LOW CALORIE DISHES ---
    {"meal_id": 1, "name": "Clear Vegetable Broth Soup", "calories": 180, "protein": 4, "carbs": 25, "fat": 2, "tags": ["Vegetarian", "Low-Carb"], "allergens": [], "price": 6.50},
    {"meal_id": 2, "name": "Sautéed Tofu & Broccoli Steamer", "calories": 290, "protein": 18, "carbs": 16, "fat": 10, "tags": ["Vegetarian", "High-Protein"], "allergens": [], "price": 9.99},
    {"meal_id": 3, "name": "Lemon Herb Poached Whitefish", "calories": 260, "protein": 28, "carbs": 4, "fat": 6, "tags": ["Non-Vegetarian", "Low-Carb"], "allergens": [], "price": 13.25},
    {"meal_id": 4, "name": "Zucchini Noodles with Pesto", "calories": 220, "protein": 6, "carbs": 12, "fat": 15, "tags": ["Vegetarian", "Antioxidant-Rich"], "allergens": [], "price": 8.50},

    # --- MEDIUM CALORIE DISHES ---
    {"meal_id": 5, "name": "Quinoa Avocado Salad Bowl", "calories": 450, "protein": 12, "carbs": 55, "fat": 18, "tags": ["Vegetarian", "Antioxidant-Rich"], "allergens": [], "price": 12.99},
    {"meal_id": 6, "name": "Spiced Paneer Protein Wrap", "calories": 500, "protein": 22, "carbs": 42, "fat": 20, "tags": ["Vegetarian", "High-Protein"], "allergens": ["Gluten"], "price": 11.00},
    {"meal_id": 7, "name": "Baked Salmon Salad with Spinach", "calories": 480, "protein": 34, "carbs": 8, "fat": 22, "tags": ["Non-Vegetarian", "High-Protein"], "allergens": [], "price": 16.50},
    {"meal_id": 8, "name": "Brown Rice and Lentil Dahl Bowl", "calories": 420, "protein": 16, "carbs": 68, "fat": 5, "tags": ["Vegetarian", "Complex-Carbs"], "allergens": [], "price": 9.25},

    # --- HIGH CALORIE DISHES ---
    {"meal_id": 9, "name": "Peanut Grilled Chicken Rice Bowl", "calories": 650, "protein": 42, "carbs": 70, "fat": 24, "tags": ["Non-Vegetarian", "High-Protein"], "allergens": ["Peanuts"], "price": 14.50},
    {"meal_id": 10, "name": "Creamy Chickpea Curry with Naan", "calories": 680, "protein": 19, "carbs": 95, "fat": 14, "tags": ["Vegetarian", "Complex-Carbs"], "allergens": ["Gluten"], "price": 11.95},
    {"meal_id": 11, "name": "Whole Wheat Mushroom Alfredo Pasta", "calories": 620, "protein": 18, "carbs": 82, "fat": 18, "tags": ["Vegetarian", "Complex-Carbs"], "allergens": ["Gluten"], "price": 12.50},
    {"meal_id": 12, "name": "Barbecue Chicken & Sweet Potato Mash", "calories": 710, "protein": 46, "carbs": 78, "fat": 16, "tags": ["Non-Vegetarian", "High-Protein"], "allergens": [], "price": 15.00}
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