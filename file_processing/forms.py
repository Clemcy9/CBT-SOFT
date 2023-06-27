from django import forms
from .models import QuestionUploads, CourseTemplate,Courses
from auth1.models import Profile


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

    def __init__(self,user, *args, **kwargs):
        super(QuestionUploadForm, self).__init__(*args, **kwargs)
        self.user = user
        self.profile = Profile.objects.get(user=user)
        self.my_courses = self.profile.courses.all()
        print(f'from quest upload--\nuser={self.user}\nprofile={self.profile}\ncourses={self.my_courses}')
        self.fields['upload'].required = True
        # this worked, but must be a list
        # self.fields['course'] = forms.ChoiceField(choices=self.my_courses)
        self.fields['course'].queryset = self.my_courses