from django import forms
from .models import UserGuess, Choice, Quiz
from django.forms.widgets import RadioSelect


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


# not working
class QuestionForm(forms.Form):
    def __init__(self, question, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        choice_list =[x for x in question[0].choice_set.all()]
        self.fields['question'] = forms.CharField(max_length=300)
        self.fields['choice'] = forms.ChoiceField(choices=choice_list,widget=RadioSelect)
        

# dashboard quiz isactive form
class DashboadQuizUpdateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields =['is_available']