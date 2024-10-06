from django import forms
from django.contrib.auth import get_user_model
from .models import *
from django import forms
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from cities_light.models import City, Region

User = get_user_model()

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'query']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'pin_code', 'state', 'city', 'address']
        widgets = {
            'phone_number': forms.NumberInput(attrs={'class': 'form-input block w-full mt-1', 'placeholder': 'Enter phone number'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-input block w-full mt-1', 'placeholder': 'Enter pin code'}),
            'state': forms.Select(attrs={'class': 'form-select block w-full mt-1'}),
            'city': forms.Select(attrs={'class': 'form-select block w-full mt-1'}),
            'address': forms.TextInput(attrs={'class': 'form-input block w-full mt-1', 'placeholder': 'Enter address'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Using Crispy Forms Helper to apply Tailwind classes
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('phone_number', css_class='block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'),
            Field('pin_code', css_class='block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'),
            Field('state', css_class='block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'),
            Field('city', css_class='block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'),
            Field('address', css_class='block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'),
            Submit('submit', 'Save', css_class='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4')
        )
