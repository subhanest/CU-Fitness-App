from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import WorkoutPlan, NutritionPlan, ProgressTracker, UserProfile
from .serializers import WorkoutPlanSerializer, NutritionPlanSerializer, ProgressTrackerSerializer, UserProfileSerializer
from .ai_suggestions import get_workout_suggestion, get_nutrition_suggestion, get_progress_percentage

# Workout Plan API
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer

    @action(detail=False, methods=['get'])
    def ai_suggestion(self, request):
        goal = request.GET.get('goal', None)

        if not goal:
            return Response({'error': 'Goal parameter is required'}, status=400)

        suggestion = get_workout_suggestion(goal)

        if not suggestion:
            return Response({'error': 'Invalid goal. Choose from muscle_gain, weight_loss, or maintain.'}, status=400)

        return Response({'suggestions': suggestion})


# Nutrition Plan API
class NutritionPlanViewSet(viewsets.ModelViewSet):
    queryset = NutritionPlan.objects.all()
    serializer_class = NutritionPlanSerializer

    @action(detail=False, methods=['get'])
    def ai_suggestion(self, request):
        meal_type = request.GET.get('meal_type', None)

        if not meal_type:
            return Response({'error': 'Meal type parameter is required'}, status=400)

        suggestion = get_nutrition_suggestion(meal_type)

        if not suggestion:
            return Response({'error': 'Invalid meal type. Choose from breakfast, lunch, or dinner.'}, status=400)

        return Response({'suggestions': suggestion})


# Progress Tracker API
class ProgressTrackerViewSet(viewsets.ModelViewSet):
    queryset = ProgressTracker.objects.all()
    serializer_class = ProgressTrackerSerializer

    @action(detail=True, methods=['get'])
    def retrieve_progress(self, request, pk=None):
        progress = self.get_object()

        # ✅ Now properly checking for goal_weight
        if not progress.goal_weight:
            return Response({'error': 'Goal weight is missing from the progress tracker.'}, status=400)

        goal_progress = get_progress_percentage(progress.weight, progress.goal_weight)

        if goal_progress is None:
            return Response({'error': 'Could not calculate progress percentage. Check weight values.'}, status=400)

        return Response({
            'weight': progress.weight,
            'body_fat_percentage': progress.body_fat_percentage,
            'muscle_mass': progress.muscle_mass,
            'goal_progress_percentage': goal_progress
        })


# User Profile API
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer