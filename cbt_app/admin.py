from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Topic,Discipline,Level,Courses,Question,Quiz,Result,Choice,Sitting

# Register your models here.

class ChoiceInline(admin.StackedInline):
    model = Choice

class TopicInline(admin.StackedInline):
    model = Topic

class QuestionInline(admin.StackedInline):
    model = Question

class QuestionAdmin(admin.ModelAdmin):
    # fields =['__all__']
    inlines = [ChoiceInline]

# class TopicAdmin(admin.ModelAdmin):
#     inlines = [QuestionInline]

# admin.site.register(User, UserAdmin)
admin.site.register([Discipline,Level,Courses,Quiz,Result,Choice,Sitting,Topic])
admin.site.register(Question,QuestionAdmin)
# admin.site.register(Topic,TopicAdmin)