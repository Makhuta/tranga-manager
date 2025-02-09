from django import forms

from database.models import API


class APIForm(forms.Form):
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    ip = forms.GenericIPAddressField(
        label="IP Address",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={"invalid": "Enter a valid IP address."},
        initial='127.0.0.1'
    )
    port = forms.IntegerField(
        label="Port",
        min_value=1,
        max_value=65535,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        initial=6531
    )
    timeout = forms.IntegerField(
        label="Timeout (s)", 
        min_value=1,
        max_value=60,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=False,
        initial=1
    )