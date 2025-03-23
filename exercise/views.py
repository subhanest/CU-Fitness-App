from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import WorkoutPlan, NutritionPlan, ProgressTracker, UserProfile
from .serializers import WorkoutPlanSerializer, NutritionPlanSerializer, ProgressTrackerSerializer, UserProfileSerializer
from .ai_suggestions import get_workout_suggestion, get_nutrition_suggestion
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Home View
def home(request):
    return render(request, 'exercise/index.html')

# ✅ WorkoutPlanViewSet (AI Workout Suggestions)
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer

    @action(detail=False, methods=['get'])
    def ai_suggestion(self, request):
        """Returns AI-based workout suggestions based on user input."""
        goal = request.GET.get('goal', None)

        if not goal:
            return Response({'error': 'Goal parameter is required'}, status=400)

        suggestion = get_workout_suggestion(goal) or []

        return Response({'suggestions': suggestion})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workout_recommendation(request):
    """Returns AI-generated structured workout recommendations."""
    goal = request.GET.get('goal', 'weight_loss')  # Default to weight loss
    suggestion = get_workout_suggestion(goal)

    if not suggestion:
        return JsonResponse({"error": "Invalid workout goal"}, status=400)

    # Ensure JSON format is correctly structured
    return JsonResponse(suggestion)



# ✅ NutritionPlanViewSet (AI Meal Suggestions)
class NutritionPlanViewSet(viewsets.ModelViewSet):
    queryset = NutritionPlan.objects.all()
    serializer_class = NutritionPlanSerializer

    @action(detail=False, methods=['get'])
    def ai_suggestion(self, request):
        """Returns AI-based meal plan based on selected meal type."""
        meal_type = request.GET.get('meal_type', None)

        if not meal_type:
            return Response({'error': 'Meal type parameter is required'}, status=400)

        suggestion = get_nutrition_suggestion(meal_type) or []

        return Response({'suggestions': suggestion})

# ✅ AI-Generated Meal Plan Recommendation (Dynamic)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meal_recommendation(request):
    """Returns AI-generated structured meal plan suggestions."""
    meal_type = request.GET.get('meal_type', 'lunch')  # Default to lunch
    suggestion = get_nutrition_suggestion(meal_type)

    if not suggestion:
        return JsonResponse({"error": "Invalid meal type selected"}, status=400)

    # Ensure JSON format is correctly structured
    return JsonResponse(suggestion)


# ✅ AI Chatbot API (Fix 403 Forbidden)
@csrf_exempt  # 🔥 Fixes 403 Forbidden Error
@api_view(['POST'])
@permission_classes([AllowAny])  # ✅ Allows chatbot to be accessed by anyone
def ai_chatbot(request):
    """Simple AI chatbot for fitness-related queries."""
    user_message = request.data.get("message", "").lower()

    # AI Chatbot Responses
    responses = {
        "hello": "Hi there! How can I assist you with your fitness goals?",
        "workout plan": "I recommend strength training and cardio. Do you want a specific plan?",
        "meal plan": "Try high-protein meals with balanced carbs and fats.",
        "bmi": "Use the calculator on our homepage to check your BMI.",
        "bye": "Goodbye! Stay fit and take care!"
    }

    bot_response = responses.get(user_message, "I'm not sure, but I can help with workouts and meals!")

    return JsonResponse({"response": bot_response})


# ✅ ProgressTrackerViewSet
class ProgressTrackerViewSet(viewsets.ModelViewSet):
    queryset = ProgressTracker.objects.all()
    serializer_class = ProgressTrackerSerializer

    @action(detail=True, methods=['get'])
    def retrieve_progress(self, request, pk=None):
        progress = self.get_object()
        return Response({
            'weight': progress.weight,
            'body_fat_percentage': progress.body_fat_percentage,
            'muscle_mass': progress.muscle_mass
        })


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import WorkoutLog

class WorkoutLogAPIView(APIView):
    permission_classes = [AllowAny]  # Use IsAuthenticated if you're using login

    def post(self, request):
        data = request.data
        try:
            workout = WorkoutLog.objects.create(
                user_id=1,  # TEMP: replace with `request.user.id` if using authentication
                exercise=data['exercise'],
                sets=data['sets'],
                reps=data['reps'],
                duration_minutes=data['duration']
            )
            return Response({"message": "Workout logged successfully!"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
        from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WorkoutLog

class WorkoutProgressAPIView(APIView):
    permission_classes = [AllowAny]  # Change to IsAuthenticated if using auth

    def get(self, request):
        try:
            logs = WorkoutLog.objects.filter(user_id=1).order_by('-date')[:5]  # Replace 1 with request.user.id if using auth
            
            if not logs.exists():
                return Response({"suggestion": "Start logging your workouts to receive personalized progress advice!"})

            # Analyze data
            total_reps = sum(log.reps for log in logs)
            total_sets = sum(log.sets for log in logs)
            total_duration = sum(log.duration_minutes for log in logs)
            count = logs.count()

            avg_reps = total_reps / count
            avg_sets = total_sets / count
            avg_duration = total_duration / count

            suggestion = (
                f"🔥 You've been averaging {avg_sets:.1f} sets of {avg_reps:.1f} reps "
                f"per workout, with {avg_duration:.1f} minutes of effort.\n"
                "💡 Suggestion: Try adding 1 more set or increase reps by 2 next session!"
            )

            return Response({"suggestion": suggestion})
        except Exception as e:
            return Response({"error": str(e)}, status=400)


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WorkoutLog

class WorkoutChartDataAPIView(APIView):
    def get(self, request):
        logs = WorkoutLog.objects.filter(user_id=1).order_by('date')  # replace 1 if using auth

        labels = [log.date.strftime('%b %d') for log in logs]
        reps = [log.reps for log in logs]
        sets = [log.sets for log in logs]
        duration = [log.duration_minutes for log in logs]

        return Response({
            "labels": labels,
            "reps": reps,
            "sets": sets,
            "duration": duration
        })



# ✅ UserProfileViewSet
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
