from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Discipline,Level,Courses,User,Question,Quiz,Result,Choice

# Register your models here.

class QuestionInline(admin.StackedInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    # fields =['__all__']
    inlines = [QuestionInline]

# admin.site.register(User, UserAdmin)
admin.site.register([Discipline,Level,Courses,Quiz,Result,Choice])
admin.site.register(Question,QuestionAdmin)
