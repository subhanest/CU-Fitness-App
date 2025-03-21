from django.shortcuts import render  # type: ignore
from django.utils.timezone import now  # type: ignore
from .ai_service import GroqAIService
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import json
from .models import CustomUser
from .models import CustomUser, UserQuestionnaire

# Create your views here.
def home(request):
    return render(request, 'myapp/index.html', {'timestamp': now().timestamp()})

def explore(request):
    return render(request, 'myApp/ER.html')  # Explore Page

def settings(request):
    return render(request, 'myApp/settings.html') # Settings Page
    
def signup_view(request):
    return render(request, 'myapp/sign__up.html')  # Sign up Page

def login_view(request):
    return render(request, 'myapp/log__in.html') # Login Page

def chatbot_view(request):
    return JsonResponse({"message": "Hello! How can I help you?"})




@csrf_exempt
def signup_view(request):
    if request.method == 'GET':
        return render(request, 'myApp/sign__up.html')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            receive_updates = data.get('receive_updates', False)
            
            # Check if user already exists
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email already exists'}, status=400)
            
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'message': 'Username already exists'}, status=400)
            
            # Create new user
            user = CustomUser.objects.create_user(
                email=email,
                username=username,
                password=password,
                receive_updates=receive_updates
            )
            
            # Log the user in
            login(request, user)
            
            # Return success with redirection to questionnaire
            return JsonResponse({
                'message': 'Sign up successful',
                'next': '/questionnaire/'
            })
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

@csrf_exempt
def login_view(request):
    if request.method == 'GET':
        return render(request, 'myApp/log__in.html')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            # Authenticate user
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
        


@csrf_exempt
def chatbot_view(request):
    if request.method == 'GET':
        return render(request, 'myapp/chatbot.html')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            ai_service = GroqAIService()
            response = ai_service.generate_response(user_message)
            
            return JsonResponse({
                'message': response,
                'status': 'success'
            })
        except Exception as e:
            return JsonResponse({
                'message': str(e),
                'status': 'error'
            }, status=500)



def questionnaire_view(request):
    """Render the questionnaire page."""
    # Check if user is authenticated, otherwise redirect to signup
    if not request.user.is_authenticated:
        return redirect('sign__up')
    
    return render(request, 'myapp/Question_list.html')

@csrf_exempt
def questionnaire_api(request):
    """API endpoint to handle questionnaire submissions."""
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Authentication required'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create or update questionnaire for user
            questionnaire, created = UserQuestionnaire.objects.get_or_create(user=request.user)
            
            # Update fields
            questionnaire.fitness_goals = data.get('fitness_goals', '')
            questionnaire.body_type = data.get('body_type', '')
            questionnaire.daily_caloric_need = data.get('daily_caloric_need') or None
            questionnaire.workout_frequency = data.get('workout_frequency', '')
            questionnaire.macronutrient_ratio = data.get('macronutrient_ratio', '')
            questionnaire.dietary_restrictions = data.get('dietary_restrictions', '')
            questionnaire.sleep_hours = data.get('sleep_hours') or None
            questionnaire.work_schedule = data.get('work_schedule', '')
            questionnaire.supplements = data.get('supplements', '')
            questionnaire.water_intake = data.get('water_intake', '')
            
            questionnaire.save()
            
            return JsonResponse({'message': 'Questionnaire saved successfully'})
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    
    return JsonResponse({'message': 'Method not allowed'}, status=405)
