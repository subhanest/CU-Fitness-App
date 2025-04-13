from django import forms
from database.models import UserQuestionnaire

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserQuestionnaire
        fields = [
            'fitness_goals',
            'current_weight',
            'target_weight',
            'activity_level',
            'cooking_time',
            'macronutrient_ratio',
            'diet',
            'intolerances',
            'daily_budget'
        ]
        widgets = {
            'fitness_goals': forms.Select(attrs={'class': 'form-control'}),
            'activity_level': forms.Select(attrs={'class': 'form-control'}),
            'macronutrient_ratio': forms.Select(attrs={'class': 'form-control'}),
            'diet': forms.RadioSelect(),
            'intolerances': forms.CheckboxSelectMultiple(),  # You may customize this in view if storing comma-separated
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'target_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'daily_budget': forms.NumberInput(attrs={'class': 'form-control'}),
        }
