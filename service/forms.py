from django import forms

class ServiceForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=200)
    command = forms.CharField(max_length=200)
    file  = forms.FileField()