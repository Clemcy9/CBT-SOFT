from django.urls import path
from .views import index, register

app_name = 'cbt_app'

urlpatterns = [
    path('', view=index, name='index'),
   
]