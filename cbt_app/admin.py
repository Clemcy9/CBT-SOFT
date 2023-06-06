from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Topic,Discipline,Level,Courses,Question,Quiz,Result,Choice,Sitting

# Register your models here.

class QuestionInline(admin.StackedInline):
    model = Choice

class TopicInline(admin.StackedInline):
    model = Topic


class QuestionAdmin(admin.ModelAdmin):
    # fields =['__all__']
    inlines = [QuestionInline]

# admin.site.register(User, UserAdmin)
admin.site.register([Discipline,Level,Courses,Quiz,Result,Choice,Sitting,Topic])
admin.site.register(Question,QuestionAdmin)
