from django import forms
# from ckeditor.widgets import CKEditorWidget
from .models import User, Profile

class RegisterForm(forms.ModelForm):
    
    class Meta:
        
        model = User
        fields = ['first_name','last_name','email','username','is_student','password']
        # exclude = []
        widgets ={
            # this helps in making password field appears as password rather than normal char field(textfield)
            'password': forms.PasswordInput(),
            'email':forms.EmailInput(attrs={'value':'-adss@gmail.com'})
        }

forms.PasswordInput

class LoginForm(forms.Form):
    
    email = forms.EmailField(required=True,initial='-adss@gmail.com')
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    # user = forms.ModelChoiceField(queryset=User.objects.all(), required=True,widget=forms.HiddenInput())
    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ['phone_number','discipline','gender','current_level','courses','about_me']
        widgets = {
            # 'profile_pics':forms.FileInput(attrs={'required':'False'}),
            # 'about_me': CKEditorWidget()
        }
