from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length=20)
    address = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'address', 'first_name', 'last_name', 'password1', 'password2']


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mt-3 ps-3 mb-3',
        'placeholder': '1234 Main Str'
    }))

    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control ps-3 mb-4',
        'placeholder': 'Apartment or suite'
    }))

    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-select form-control mt-2 mb-4'
    }))

    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mt-3 ps-3 mb-4',
        'placeholder': 'Town/City'
    }))

    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mt-2 mb-4 ps-3'
    }))



