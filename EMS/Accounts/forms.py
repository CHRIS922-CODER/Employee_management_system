from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.forms import Form
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.contrib import messages

class CreationUserForm(UserCreationForm):
    username = forms.CharField(label='username',min_length=5,max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)

    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.exists():
            messages.error(self.request,'User Already Exist',extra_tags='error')
            raise ValidationError('User Already Exist')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.exists():
            messages.error(self.request,'Email Already Exist',extra_tags='error')
            raise ValidationError('Email Already Exist')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            messages.error(self.request,'Password does not match',extra_tags='error')
            raise ValidationError('Password does not match')
        return password2
    
    def save(self,commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
    
        
    


