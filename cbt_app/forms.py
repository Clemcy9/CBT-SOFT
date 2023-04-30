from django import forms
from .models import UserGuess, Choice, Profile


# class RegisterForm(forms.ModelForm):
    
#     class Meta:
        
#         model = User
#         fields = ['first_name','last_name','email','username','is_student','password']
#         # exclude = []

# class QuizForm(forms.ModelForm):
    
#     class Meta:
#         model = UserGuess
#         fields =['question', 'guess']

#         widgets ={
#             'guess': forms.RadioSelect
#         }

class QuizForm(forms.Form):
    question = forms.CharField()
    choice = forms.BooleanField()

    # guess =forms.ModelChoiceField(queryset=None)

    # def __init__(self,*args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['option'].queryset = Choice.objects.filter(question = )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'