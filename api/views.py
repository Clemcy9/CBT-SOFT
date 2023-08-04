from django.shortcuts import render
from rest_framework import viewsets
from .serializers import QuestionSerializer
from cbt_app.models import Question, Quiz
# Create your views here.


class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.order_by('?')
    serializer_class = QuestionSerializer
    