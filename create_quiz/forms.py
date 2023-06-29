from django import forms
from auth1.models import Profile
from cbt_app.models import Courses, Topic


class CreateByTopicForm(forms.Form):
    title = forms.CharField(max_length=100, help_text='name of the quiz')
    course = forms.ModelChoiceField(queryset=Courses.objects.all())
    topic = forms.ModelChoiceField(queryset=Topic.objects.all())
    max_no_question = forms.IntegerField()
    duration = forms.FloatField(help_text='enter duration in minutes', required=True,)
    activate = forms.BooleanField(required=False)
    class Meta:
        widgets = {
                "upload" : forms.FileInput(attrs={
                    'accept':'.xlsx', 
                    'class':'form-control', 
                    # 'required':True
                }),
                
            }

    def __init__(self, *args, user, **kwargs):
        super(CreateByTopicForm, self).__init__(*args, **kwargs)
        self.user = user
        self.profile = Profile.objects.get(user=user)
        self.my_courses = self.profile.courses.all()
        print(f'from quest upload--\nuser={self.user}\nprofile={self.profile}\ncourses={self.my_courses}')
        # this worked, but must be a list
        # self.fields['course'] = forms.ChoiceField(choices=self.my_courses)
        self.fields['course'].queryset = self.my_courses