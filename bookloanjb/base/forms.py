from django import forms
from django.contrib.auth.models import User
from base.models import UserProfileInfo
from django.core import validators


# User forms
class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())  # Password field for user registration
    verify_pass = forms.CharField(widget=forms.PasswordInput())    

    class Meta():
        model = User  # Use the User model
        fields = ("username","email","password")

    def clean(self):
        all_clean_data = super().clean()
        password = all_clean_data['password']
        verify_pass = all_clean_data['verify_pass']

        if password != verify_pass:
            raise forms.ValidationError("passwords do not match")
        
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo  # Use the UserProfileInfo model
        fields = ("profile_pic",)
