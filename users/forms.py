# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'userType', 'first_name', 'last_name', 'email')
        # fields = ('username', 'userType','PIN','first_name', 'last_name', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'userType', 'first_name', 'last_name', 'email')
        # fields = ('username', 'userType', 'PIN', 'first_name', 'last_name', 'email')
