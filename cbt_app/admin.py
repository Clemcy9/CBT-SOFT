from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Discipline,Level,Courses,Question,Quiz,Result,Choice,Sitting

# Register your models here.

class QuestionInline(admin.StackedInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    # fields =['__all__']
    inlines = [QuestionInline]

# admin.site.register(User, UserAdmin)
admin.site.register([Discipline,Level,Courses,Quiz,Result,Choice,Sitting])
admin.site.register(Question,QuestionAdmin)
