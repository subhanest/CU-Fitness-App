from django.contrib import admin
from .models import CustomUser, UserQuestionnaire, UserSession, MealLog

admin.site.register(CustomUser)
admin.site.register(UserQuestionnaire)
admin.site.register(UserSession)
admin.site.register(MealLog)