from django.urls import path
from .views import index, dashboard, take_quiz

app_name = 'cbt_app'

urlpatterns = [
    path('', view=index, name='index'),
    path('dashboard/',view=dashboard, name='dashboard'),
    path('takequiz/<int:quiz_id>',view=take_quiz, name='take_quiz')
   
]