from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, blank=False)
    # username = models.CharField(unique=True, max_length=30)
    # password = models.CharField(max_length=128, )
    is_student = models.BooleanField('Are you a student?',blank=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username','is_student']
