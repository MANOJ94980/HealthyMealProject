# test_main.py
from fastapi.testclient import TestClient
from main import app

# Create a test client that can simulate user clicks on our API
client = TestClient(app)

def test_vegetarian_recommendation():
    """
    Automated Test 1: Verifies that a Vegetarian request 
    only returns Vegetarian meals.
    """
    response = client.post("/api/recommendations", json={
        "user_id": 1,
        "name": "Niharika",
        "target_calories": 1500,
        "dietary_restriction": "Vegetarian",
        "allergies": []
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that every single meal returned is tagged 'Vegetarian'
    for meal in data["recommended_meals"]:
        assert "Vegetarian" in meal["tags"]

def test_low_calorie_fallback():
    """
    Automated Test 2: Verifies that the new low calorie items 
    populate when targets drop under 900.
    """
    response = client.post("/api/recommendations", json={
        "user_id": 2,
        "name": "Varshini",
        "target_calories": 850,
        "dietary_restriction": "Vegetarian",
        "allergies": []
    })
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["recommended_meals"]) > 0