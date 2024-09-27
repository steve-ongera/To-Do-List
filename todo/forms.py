from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirmpassword = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("confirmpassword")

        # Ensure the two passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn’t match.")

        return cleaned_data

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'message_text', 'completed']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']  # Add other fields as needed

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # You can add more fields if needed
