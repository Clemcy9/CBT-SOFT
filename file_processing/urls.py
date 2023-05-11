from django.urls import path
from .views import question_upload

app_name = 'file_processing'

urlpatterns=[
    path('question_upload/',view=question_upload,name='question_upload')
]