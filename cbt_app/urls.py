from django.urls import path
from .views import index, dashboard, take_quiz, quiz_progress,api_all_question

app_name = 'cbt_app'

urlpatterns = [
    path('', view=index, name='index'),
    path('dashboard/',view=dashboard, name='dashboard'),
    path('takequiz/<int:quiz_id>',view=take_quiz, name='take_quiz'),
    path('progress/', view=quiz_progress, name='quiz_progress'),
    path('api/', view=api_all_question, name='api'),
   
]