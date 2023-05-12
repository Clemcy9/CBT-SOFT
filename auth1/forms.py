from django import forms
from .models import User, Profile

class RegisterForm(forms.ModelForm):
    
    class Meta:
        
        model = User
        fields = ['first_name','last_name','email','username','is_student','password']
        # exclude = []
        widgets ={'password': forms.PasswordInput()}

# this helps in making password field appears as password rather than normal char field(textfield)
forms.PasswordInput

class LoginForm(forms.Form):
    
    email = forms.EmailField(required=True,initial='-adsc@gmail.com')
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ['phone_number','discipline','current_level','courses','profile_pics']