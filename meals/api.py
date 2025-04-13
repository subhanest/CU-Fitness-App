
import requests
API_KEY = "49299ae170984342ba0757ef38a15ead"

def get_daily_meal_plan(calories, diet=None, intolerances=None, max_ready_time=None, macro_pref=None):
    url = "https://api.spoonacular.com/mealplanner/generate"
    params = {
        "timeFrame": "day",
        "targetCalories": calories,
        "apiKey": API_KEY
    }

    if diet:
        params["diet"] = diet
    if intolerances:
        params["intolerances"] = intolerances

    response = requests.get(url, params=params)
    data = response.json()

    meals = []
    for idx, meal in enumerate(data.get("meals", [])):
        meal_type = ["Breakfast", "Lunch", "Dinner"][idx] if idx < 3 else "Meal"
        # Skip meals over the max ready time (manual filtering)
        too_long = False
        if max_ready_time:
            allowed_limit = int(max_ready_time * 1.2)
            if meal.get("readyInMinutes", 0) > allowed_limit:
                too_long = True

        # Get detailed nutrition and ingredients
        detail_url = f"https://api.spoonacular.com/recipes/{meal['id']}/information"
        detail_params = {"includeNutrition": True, "apiKey": API_KEY}
        detail_res = requests.get(detail_url, params=detail_params)
        detail_data = detail_res.json()

        nutrients = {
    n['title'].lower(): n['amount']
    for n in detail_data.get("nutrition", {}).get("nutrients", [])
    if 'title' in n and 'amount' in n
        }

        ingredients = [
            i['original']
            for i in detail_data.get("extendedIngredients", [])
        ]

        # Optional macronutrient filter
        passes_macro_filter = True
        if macro_pref and nutrients:
            protein = nutrients.get("protein", 0)
            carbs = nutrients.get("carbohydrates", 0)
            fat = nutrients.get("fat", 0)
            total = protein + carbs + fat
            if total > 0:
                protein_pct = protein / total
                carb_pct = carbs / total
                fat_pct = fat / total

                if macro_pref == "high_protein" and protein_pct < 0.3:
                    passes_macro_filter = False
                elif macro_pref == "low_carb" and carb_pct > 0.4:
                    passes_macro_filter = False
                elif macro_pref == "low_fat" and fat_pct > 0.35:
                    passes_macro_filter = False

        if passes_macro_filter:
            meals.append({
            "title": meal["title"],
            "calories": nutrients.get("calories") or detail_data.get("nutrition", {}).get("nutrients", [{}])[0].get("amount", 0),
            "readyInMinutes": meal.get("readyInMinutes"),
            "pricePerServing": detail_data.get("pricePerServing", 0) / 100,
            "meal_type": meal_type,
            "instructions": detail_data.get("instructions", "No instructions provided."),
            "ingredients": ingredients,
            "is_slow": too_long,
            })

    return meals

def fetch_calories_from_spoonacular(food_name):
    api_key = "49299ae170984342ba0757ef38a15ead"  # your Spoonacular key
    url = "https://api.spoonacular.com/food/ingredients/search"
    params = {
        "query": food_name,
        "number": 1,
        "apiKey": api_key,
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("results"):
            food_id = data["results"][0]["id"]
            detail_url = f"https://api.spoonacular.com/food/ingredients/{food_id}/information"
            detail_params = {"amount": 1, "unit": "serving", "apiKey": api_key}
            detail_response = requests.get(detail_url, params=detail_params)
            detail_data = detail_response.json()

            nutrients = detail_data.get("nutrition", {}).get("nutrients", [])
            for n in nutrients:
                if n.get("name") == "Calories":
                    return round(n.get("amount", 0))
    except Exception as e:
        print(f"Error fetching calories from Spoonacular: {e}")

    return None  # fallback
