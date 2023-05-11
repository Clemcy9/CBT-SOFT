from django.db import models
from django.conf import settings
from cbt_app.models import Courses, Level

# Create your models here.

class QuestionUploads(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    course = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=100)
    file = models.FileField('Excel file',upload_to='./static/uploads')
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.course + self.title

class CourseTemplate(models.Model):
    course = models.OneToOneField(Courses, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.course
    