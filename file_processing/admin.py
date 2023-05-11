from django.contrib import admin
from .models import QuestionUploads, CourseTemplate

# Register your models here.

admin.site.register([QuestionUploads,CourseTemplate])
