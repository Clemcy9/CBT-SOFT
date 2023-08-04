from rest_framework import serializers
from cbt_app.models import Quiz, Question, Choice

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','content','choice_set']
