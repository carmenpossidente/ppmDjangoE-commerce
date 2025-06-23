from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_store_manager')
    list_filter = ('is_store_manager',)
    fieldsets = UserAdmin.fieldsets + (
        ('Store Manager', {'fields': ('is_store_manager',)}),
        ('Informazioni aggiuntive', {'fields': ('phone_number', 'birth_date', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)