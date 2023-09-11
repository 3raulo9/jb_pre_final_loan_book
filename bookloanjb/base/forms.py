# Import necessary modules
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from base.models import Review

# User forms
class UserForm(forms.ModelForm):
    # Define form fields
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())  # Password field for user registration
    verify_pass = forms.CharField(widget=forms.PasswordInput())    

    class Meta():
        model = User  # Use the User model
        fields = ("username","password")

    def clean(self):
        # Clean and validate form data
        all_clean_data = super().clean()
        password = all_clean_data['password']
        verify_pass = all_clean_data['verify_pass']

        if password != verify_pass:
            raise forms.ValidationError("Passwords do not match")
        

class ReviewForm(forms.ModelForm):
    # Define review text field with custom attributes
    text_field = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'message',
        'placeholder': 'Your review here...',
        'required': '',
    }))

    class Meta():
        model = Review
        fields = ("text_field",)
