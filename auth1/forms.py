from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    
    class Meta:
        
        model = User
        fields = ['first_name','last_name','email','username','is_student','password']
        # exclude = []
        widgets ={'password': forms.PasswordInput()}

# this helps in making password field appears as password rather than normal char field(textfield)
forms.PasswordInput

class LoginForm(forms.Form):
    
    email = forms.EmailField(required=True,initial='@gmail.com')
    password = forms.CharField(widget=forms.PasswordInput)