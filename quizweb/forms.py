from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from quiz.models import Category,Questions,Answers

class RegistrationForm(UserCreationForm):
    
    class Meta:
        model=User
        fields=['email','username','password1','password2']


class SignInForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()


