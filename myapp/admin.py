from django.contrib import admin

from .models import User

admin.site.register(User)  # This makes User appear in the admin panel
