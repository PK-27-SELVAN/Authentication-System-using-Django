from django.contrib import admin
from .models import customUser

# Register your models here.
@admin.register(customUser)
class customeuseradmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','username', 'email','phone']