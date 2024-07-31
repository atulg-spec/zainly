from django import forms
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'query']