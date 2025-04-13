from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import UserPreferenceForm
from database.models import UserQuestionnaire
from .utils import calculate_target_calories
from .api import get_daily_meal_plan
from database.models import MealLog
from datetime import date
from .api import fetch_calories_from_spoonacular
from django.shortcuts import get_object_or_404
from django.db.models import Sum

@login_required
def nutrition_index(request):
    user = request.user
    target_calories = None
    try:
        questionnaire = UserQuestionnaire.objects.get(user=user)
    except UserQuestionnaire.DoesNotExist:
        questionnaire = UserQuestionnaire(user=user)

        

    if request.method == 'POST':
        if request.POST.get('meal_log_flag') == 'true':
            food_names = request.POST.getlist("food_name[]")
            quantities = request.POST.getlist("quantity[]")
            times = request.POST.getlist("time[]")
            meal_types = request.POST.getlist("meal_type[]")
            calories = request.POST.getlist("calories[]")
            meal_date = request.POST.get("meal_date")

            for i in range(len(food_names)):
                food = food_names[i].strip()
                quantity = int(quantities[i])
                time_eaten = times[i]
                meal_type = meal_types[i]
                calorie_val = calories[i]

                if calorie_val:
                 final_calories = float(calorie_val)
                else:
                    fetched_calories = fetch_calories_from_spoonacular(food)
                    final_calories = fetched_calories if fetched_calories is not None else 0

      

                MealLog.objects.create(
                    user=user,
                    food_name=food,
                    quantity=quantity,
                    time=time_eaten,
                    date=meal_date,
                    meal_type=meal_type,
                    calories=final_calories
                )
            return redirect('nutrition_index')
    form = UserPreferenceForm(request.POST, instance=questionnaire)
    if form.is_valid():
            preferences = form.save(commit=False)
            preferences.intolerances = ",".join(request.POST.getlist('intolerances'))
            preferences.save()
    
            # reload updated values from DB
            questionnaire.refresh_from_db()
            form = UserPreferenceForm(instance=questionnaire)

    else:
        form = UserPreferenceForm(instance=questionnaire)
    if questionnaire.intolerances:
            form.fields['intolerances'].initial = questionnaire.intolerances.split(',')
    today = date.today()
    logged_meals = MealLog.objects.filter(user=user, date=today).order_by('-time')
    daily_calories = MealLog.objects.filter(user=user, date=today).aggregate(
            total=Sum('calories')
    )['total'] or 0  # fallback to 0 if no meals found
    # Calculate target calories (regardless of GET or POST)
    if (
        user.age and user.gender and
        questionnaire.current_weight and questionnaire.height and
        questionnaire.activity_level and questionnaire.fitness_goals
    ):
        target_calories = calculate_target_calories(
            age=user.age,
            gender=user.gender,
            weight=questionnaire.current_weight,
            height=questionnaire.height,
            activity_level=questionnaire.activity_level,
            goal=questionnaire.fitness_goals
        )

        questionnaire.target_calories = target_calories
        questionnaire.save()
        # Load meal plan data from session, if available
    meals = request.session.pop('spoonacular_meals', None)
    total_cost = request.session.pop('total_cost', None)
    daily_budget = request.session.pop('daily_budget', None)
    over_budget = request.session.pop('over_budget', None)
    meal_plan_message = request.session.pop ('meal_plan_message', None)

    return render(request, 'meals/nutrition_index.html', {
        'form': form,
        'target_calories': target_calories,
        'message': 'Preferences saved successfully!' if request.method == 'POST' else None,
        'logged_meals': logged_meals,
        'today_date': today,
        'spoonacular_meals': meals,
        'total_cost': total_cost,
        'daily_budget': daily_budget,
        'over_budget': over_budget,
        'message': meal_plan_message or ('Preferences saved successfully!' if request.method == 'POST' else None),
        'daily_calories': daily_calories,
        'current_weight': questionnaire.current_weight,
        'target_weight': questionnaire.target_weight,
    })


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Optional reset command
        if user_message.strip().lower() in ["reset", "restart", "clear"]:
            request.session.flush()
            return JsonResponse({
                "response": "Okay, let's start fresh! How can I help you with your nutrition today?"
            })

        # Initialize chat history in session
        if "chat_history" not in request.session:
            request.session["chat_history"] = []
            request.session["conversation_started"] = True

        chat_history = request.session["chat_history"]

        # Include the last 5 exchanges in the prompt
        instruction_blocks = ""
        for exchange in chat_history[-5:]:
            instruction_blocks += f"### Instruction:\n{exchange['user']}\n\n### Response:\n{exchange['bot']}\n\n"

        # Add current message to the prompt
        instruction_blocks += f"### Instruction:\n{user_message}\n\n### Response:\n"

        # Hugging Face API setup
        api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
        headers = {
            "Authorization": "Bearer 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"
        }
        payload = {
            "inputs": instruction_blocks
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload)

            if response.status_code == 200:
                try:
                    result = response.json()
                    raw_text = result[0].get("generated_text", "")
                    if "### Response:" in raw_text:
                        bot_message = raw_text.split("### Response:")[-1].strip()
                    else:
                        bot_message = raw_text.strip()
                except Exception:
                    bot_message = "Sorry, the model returned an unexpected response."
            else:
                bot_message = f"Error {response.status_code}: {response.text}"

        except Exception as e:
            bot_message = f"Error: {str(e)}"

        # Save the latest exchange
        chat_history.append({"user": user_message, "bot": bot_message})
        request.session["chat_history"] = chat_history

        return JsonResponse({"response": bot_message})
   
    from .forms import UserPreferenceForm  # already imported above

@login_required
def generate_meal_plan(request):
    user = request.user

    try:
        questionnaire = UserQuestionnaire.objects.get(user=user)
    except UserQuestionnaire.DoesNotExist:
        questionnaire = None

    meals = []
    if questionnaire and questionnaire.target_calories:
        meals = get_daily_meal_plan(
            calories=questionnaire.target_calories,
            diet=questionnaire.diet,
            intolerances=questionnaire.intolerances,
            max_ready_time=questionnaire.cooking_time,
            macro_pref=questionnaire.macronutrient_ratio
        )
        total_cost = sum(meal.get("pricePerServing", 0) for meal in meals)
        daily_budget = questionnaire.daily_budget or 0 
        over_budget = total_cost - daily_budget if total_cost > daily_budget else 0

        request.session['spoonacular_meals'] = meals
        request.session['total_cost'] = total_cost
        request.session['daily_budget'] = daily_budget
        request.session['over_budget'] = over_budget
        request.session['meal_plan_message'] = 'Meal plan generated successfully!'

        return redirect('nutrition_index') 


@login_required
def edit_meal(request, meal_id):
    if request.method == "POST":
        meal = get_object_or_404(MealLog, id=meal_id, user=request.user)
        new_calories = request.POST.get("updated_calories")
        if new_calories:
            meal.calories = float(new_calories)
            meal.save()
        return redirect('nutrition_index')
