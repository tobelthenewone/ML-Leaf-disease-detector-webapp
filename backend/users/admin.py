from django.contrib import admin
from users.models import NewUser,Prediction, Disease
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'user_name', 'first_name',)
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )

class PredictionConfig(admin.ModelAdmin):  # Corrected class name
    model = Prediction
    list_filter = ('imageName', 'image', 'diseases', 'severity', 'scanned')
    list_display = ('imageName', 'image', 'severity', 'scanned')


admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Prediction, PredictionConfig)  # Use the corrected class name
admin.site.register(Disease)
