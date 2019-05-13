from django.contrib import admin
# from django.conf import settings
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id']
    
admin.site.register(User, UserAdmin)