def calculate_target_calories(age, gender, weight, height, activity_level, goal):
    # Step 1: BMR using Mifflin-St Jeor Equation
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:  # female or other
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Step 2: Activity multiplier
    activity_factors = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    tdee = bmr * activity_factors.get(activity_level, 1.55)

    # Step 3: Adjust for goal
    if goal == 'lose':
        return round(tdee * 0.85)
    elif goal == 'gain':
        return round(tdee * 1.15)
    else:  # maintain
        return round(tdee)