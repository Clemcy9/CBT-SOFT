from django import forms
import random

# class QuizForm(forms.Form):
#     question = forms.CharField()
#     choice = forms.BooleanField()

    # guess =forms.ModelChoiceField(queryset=None)

    # def __init__(self,*args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['option'].queryset = Choice.objects.filter(question = )
    # self.fields['course'] = forms.ChoiceField(choices=self.my_courses)

class QuestionChoiceForm(forms.Form):
    question = forms.CharField(max_length=255,)
    choice = forms.ChoiceField

    def __init__(self, *args,quest, **kwargs):
        self.quest = quest
        super().__init__(*args, **kwargs)

        self.mylist = [x for x in quest.choice_set.all()]
        random.shuffle(self.mylist)
        self.choices = [(x.is_answer, x) for x in self.mylist ]
        self.fields['question'] = forms.CharField(label = self.quest, empty_value=quest.id)
        self.fields['choice'] = forms.ChoiceField(choices=self.choices,widget=forms.RadioSelect())