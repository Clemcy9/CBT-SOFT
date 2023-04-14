from django.urls import path
from .views import index, register



urlpatterns = [
    path('', view=index, name='home'),
    path('reg/', view=register, name='register'),
   
]