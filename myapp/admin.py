<<<<<<< HEAD
=======
# from django.contrib import admin

# from .models import User

# admin.site.register(User)  # This makes User appear in the admin panel


# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.utils.translation import gettext_lazy as _
# from .models import CustomUser, UserSession


# class CustomUserAdmin(UserAdmin):
#     """Custom user admin for the CustomUser model."""
    
#     list_display = ('email', 'username', 'is_active', 'is_staff', 'date_joined')
#     list_filter = ('is_active', 'is_staff', 'receive_updates')
#     search_fields = ('email', 'username')
#     ordering = ('email',)
    
#     fieldsets = (
#         (None, {'fields': ('email', 'username', 'password')}),
#         (_('Permissions'), {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         (_('Personal info'), {'fields': ('receive_updates',)}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
    
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'password1', 'password2'),
#         }),
#     )


# class UserSessionAdmin(admin.ModelAdmin):
#     """Admin configuration for the UserSession model."""
    
#     list_display = ('user', 'created_at', 'expires_at')
#     list_filter = ('created_at', 'expires_at')
#     search_fields = ('user__email', 'user__username')
#     date_hierarchy = 'created_at'


# # Register models with the admin site
# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(UserSession, UserSessionAdmin)

>>>>>>> 66365f4796147ac91538717360efc7a2bb903171
from django.contrib import admin
from .models import CustomUser, UserQuestionnaire, UserSession

admin.site.register(CustomUser)
admin.site.register(UserQuestionnaire)
admin.site.register(UserSession)