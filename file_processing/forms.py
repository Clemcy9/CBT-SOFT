from django import forms
from .models import QuestionUploads, CourseTemplate

class QuestionUploadForm(forms.ModelForm):
    # upload = forms.FileField(required=False, )
    duration = forms.FloatField(help_text='enter duration in minutes', required=True,)
    activate = forms.BooleanField()
    class Meta:
        model =QuestionUploads
        fields = ['course','title','upload']
        # fields = '__all__'
    
        widgets = {
                "upload" : forms.FileInput(attrs={
                    'accept':'.xlsx', 
                    'class':'form-control', 
                    # 'required':True
                }),
            }

    def __init__(self, *args, **kwargs):
        super(QuestionUploadForm, self).__init__(*args, **kwargs)
        self.fields['upload'].required = True