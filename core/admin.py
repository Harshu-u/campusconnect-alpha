from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User # Import your custom User model

# Optional: Customize how the User model appears in the admin
class CustomUserAdmin(UserAdmin):
    model = User
    # Add 'role' to the display and editing fields
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role', 'profile_image_url')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role', 'profile_image_url')}),
    )

# Register your custom User model with the custom admin class
admin.site.register(User, CustomUserAdmin)