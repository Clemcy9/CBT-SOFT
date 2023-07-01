from django.urls import path
from .views import index, dashboard, take_quiz, quiz_progress,api_all_question,result_list, update_timeleft, api_edit_quiz

app_name = 'cbt_app'

urlpatterns = [
    path('', view=index, name='index'),
    path('dashboard/',view=dashboard, name='dashboard'),
    path('takequiz/<int:quiz_id>',view=take_quiz, name='take_quiz'),
    path('progress/', view=quiz_progress, name='quiz_progress'),
    path('result_list/<int:quiz_id>', view=result_list, name='result_list'),
    path('api/', view=api_all_question, name='api'),
    path('api_edit_quiz/', view=api_edit_quiz, name='api_edit_quiz'),
    path('update_timeleft/<int:quiz_id>', view = update_timeleft, name = 'time_update')
   
]

