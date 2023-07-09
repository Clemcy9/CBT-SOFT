from django.urls import path, include
from django.views.generic import RedirectView
from .views import create_quiz_by_topic, get_topics

app_name = 'create_quiz'

urlpatterns=[
    path('by_topic', view = create_quiz_by_topic, name='by_topic'),
    path('api_topics', view= get_topics, name='get_topics')

]