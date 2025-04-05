import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from database.models import CustomUser, UserQuestionnaire


class Command(BaseCommand):
    help = 'Generate 50 test users with questionnaires'

    # Sample data pools for randomization
    FITNESS_GOALS = ["Weight loss", "Muscle gain", "Endurance", "Flexibility", "General health"]
    BODY_TYPES = ["Lean", "Athletic", "Endomorph", "Ectomorph", "Mesomorph"]
    WORKOUT_FREQUENCIES = ["3 days/week, Moderate", "5 days/week, High Intensity", "Daily, Light", "2 days/week, Low"]
    MACRO_RATIOS = ["High protein, Low carb", "Balanced", "High carb, Low fat", "Keto"]
    DIETARY_RESTRICTIONS = ["None", "Vegetarian", "Gluten-free", "Vegan", "Nut allergy"]
    WORK_SCHEDULES = ["9-5 Job", "Student", "Shift Work", "Freelancer", "Unemployed"]
    SUPPLEMENTS = ["None", "Protein", "Creatine", "Multivitamin", "Fish oil"]
    WATER_INTAKES = ["2 liters", "3 liters", "1.5 liters", "4 liters", "2.5 liters"]

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating 50 test users with questionnaires...")

        for i in range(50):
            # Create a unique user
            email = f"testuser{i+1}@cufitness.co"
            username = f"user_{i+1}"
            password = "testuser123"

            user = CustomUser.objects.create_user(
                email=email,
                username=username,
                password=password,
                phone=f"123-456-00{i:02d}" if random.choice([True, False]) else None,  # Optional phone
                age=random.randint(18, 65) if random.choice([True, False]) else None,  # Optional age
                gender=random.choice(["Male", "Female", "Other"]) if random.choice([True, False]) else None,  # Optional gender
                receive_updates=random.choice([True, False]),
                date_joined=timezone.now(),
            )
            self.stdout.write(f"Created user: {user.email}")

            # Create a questionnaire for the user (all fields required)
            UserQuestionnaire.objects.create(
                user=user,
                fitness_goals=random.choice(self.FITNESS_GOALS),
                body_type=random.choice(self.BODY_TYPES),
                daily_caloric_need=random.randint(1500, 3000),
                workout_frequency=random.choice(self.WORKOUT_FREQUENCIES),
                macronutrient_ratio=random.choice(self.MACRO_RATIOS),
                dietary_restrictions=random.choice(self.DIETARY_RESTRICTIONS),
                sleep_hours=random.randint(5, 9),
                work_schedule=random.choice(self.WORK_SCHEDULES),
                supplements=random.choice(self.SUPPLEMENTS),
                water_intake=random.choice(self.WATER_INTAKES),
            )
            self.stdout.write(f"Created questionnaire for: {user.email}")

        self.stdout.write(self.style.SUCCESS("Successfully generated 50 test users with questionnaires!"))