from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

HEALTH_WARNINGS = {
    "diabetic": ["sugar", "chocolate", "honey"],
    "lactose": ["milk", "cheese", "butter"],
    "weightloss": ["fried", "cream", "butter"],
    "gym": [],
    "vegetarian": ["chicken", "fish", "meat"]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/planner')
def planner():
    return render_template('planner.html')

@app.route('/generate', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get('ingredients', '')
    health_mode = data.get('healthMode', '')
    mode = data.get('mode', 'normal')

    if not ingredients:
        return jsonify([])

    search_term = ingredients.split(',')[0].strip()
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={search_term}"

    response = requests.get(url).json()
    meals = response.get('meals', [])

    user_ingredients = [i.strip().lower() for i in ingredients.split(',') if i.strip()]
    results = []

    for meal in meals[:5]:
        instruction_text = meal.get('strInstructions', '').lower()
        warnings = []

        if health_mode in HEALTH_WARNINGS:
            for item in HEALTH_WARNINGS[health_mode]:
                if item in instruction_text:
                    warnings.append(item)

        matched = [item for item in user_ingredients if item in instruction_text]
        missing = [item for item in user_ingredients if item not in instruction_text]

        match_percent = int((len(matched) / max(len(user_ingredients), 1)) * 100)
        quick_badge = "⏱ Ready in 15–20 mins" if mode == "leftover" else "🍽 Chef Special"

        results.append({
            "name": meal["strMeal"],
            "image": meal["strMealThumb"],
            "category": meal["strCategory"],
            "instructions": meal["strInstructions"][:220] + "...",
            "calories": "Approx 300–500 kcal",
            "protein": "10–20g",
            "match_percent": match_percent,
            "missing": missing,
            "warning": warnings,
            "badge": quick_badge
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)