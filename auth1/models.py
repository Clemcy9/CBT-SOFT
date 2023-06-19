from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
from ckeditor.fields import RichTextField
from cbt_app.models import Discipline, Courses, Level
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, blank=False)
    is_student = models.BooleanField('Are you a student?',blank=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username','is_student']

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User,default=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(blank=True, max_length=16)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True)
    courses = models.ManyToManyField(Courses)
    current_level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    profile_pics = models.ImageField('Profile Picture',upload_to='./static/profile', null=True)
    about_me = RichTextField(blank=True,null=True)
    def __str__(self):
        return str(self.user)
    
    def to_dict(self):
        return {
            'user':self.user,
            'phone_number':self.phone_number,
            'discipline':self.discipline,
            'courses':self.courses,
            'current_level':self.current_level,
            'about_me': self.about_me
        }
    
