from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    
    class Meta:
        
        model = User
        fields = ['first_name','last_name','email','username','is_student','password']
        # exclude = []

forms.PasswordInput

class LoginForm(forms.Form):
    
    email = forms.EmailField(required=True,initial='name@gmail.com')
    password = forms.CharField(widget=forms.PasswordInput)