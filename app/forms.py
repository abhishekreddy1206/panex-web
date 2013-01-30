from django import forms
import app.models
from django.forms.util import ErrorList


class AppForm(forms.Form):
    name = forms.CharField(max_length=100, 
    	help_text=u'Enter a name for the App')
    description = forms.CharField(max_length=200,
    	help_text=u'Enter a description',
    	widget=forms.Textarea)
    author = forms.CharField(max_length=200,
    	help_text="Author for the App")
    version = forms.IntegerField()
    file = forms.FileField()
