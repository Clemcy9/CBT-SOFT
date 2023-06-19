from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile

class ProfileAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    


admin.site.register([Profile])
admin.site.register(User, UserAdmin)