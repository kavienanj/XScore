from django import forms
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]
        widgets = {field: forms.TextInput(attrs={
            'class': 'form-control',
            'required': 'True',
        }) for field in fields}
        # widgets['email'] = forms.TextInput(attrs={'type': 'email', 'class': 'form-control','required': 'True',})

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    '''def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count():
            raise forms.ValidationError("User with email already exists")
        page = requests.get(f'https://api.trumail.io/v2/lookups/json?email={email}')
        if not page.json()['deliverable']:
            raise forms.ValidationError("Invalid Email, Doesn't exist!")
        return email'''


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
