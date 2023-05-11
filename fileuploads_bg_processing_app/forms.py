from django import forms
from .models import QuestionUploads, CourseTemplate

class QuestionUploadForm(forms.ModelForm):
    class Meta:
        model =QuestionUploads
        fields = ['course','title','file']