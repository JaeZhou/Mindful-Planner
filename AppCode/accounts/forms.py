from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # Metadata for Django user
    class Meta: 
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def clean(self):

        cleaned_data = super().clean()
        
        return cleaned_data