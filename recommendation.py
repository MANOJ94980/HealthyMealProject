# recommendation.py

def generate_diet_plan(user_profile: dict, available_meals: list) -> list:
    """
    Filters meals based on calories, restrictions, and dynamically assigns 
    a custom health benefit reason detailing why that food is useful.
    """
    target_calories_per_meal = user_profile.get("target_calories", 2000) / 3
    user_allergies = set(user_profile.get("allergies", []))
    dietary_tag = user_profile.get("dietary_restriction")

    recommended_meals = []

    for meal in available_meals:
        # 1. Allergen filtering
        meal_allergens = set(meal.get("allergens", []))
        if user_allergies.intersection(meal_allergens):
            continue 
        
        # 2. Dietary restriction filtering (Vegetarian alignment)
        if dietary_tag and dietary_tag not in meal.get("tags", []):
            continue

        # 3. Caloric target window matching (+/- 150 calories)
        if abs(meal["calories"] - target_calories_per_meal) <= 150:
            # Create a shallow copy of the meal so we don't alter the master database array
            custom_meal = meal.copy()
            
            # Dynamically attach a helpful explanation based on the meal type
            if "High-Protein" in custom_meal["tags"]:
                custom_meal["why_useful"] = "Excellent for muscle recovery and sustaining metabolic health without overshooting caloric bounds."
            elif "Low-Carb" in custom_meal["tags"]:
                custom_meal["why_useful"] = "Maintains steady blood sugar levels and prevents post-meal fatigue, matching low-calorie requirements."
            elif "Antioxidant-Rich" in custom_meal["tags"]:
                custom_meal["why_useful"] = "Packed with essential micronutrients and vitamins that boost immune function and lower cell inflammation."
            else:
                custom_meal["why_useful"] = "Provides clean, complex carbohydrates for prolonged endurance and sustained daily energy release."
                
            recommended_meals.append(custom_meal)

    return recommended_meals