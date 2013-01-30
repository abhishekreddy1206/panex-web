from django import forms
import service.models
from django.forms.util import ErrorList


class ServiceForm(forms.Form):
    name = forms.CharField(max_length=100, 
    	help_text=u'Enter a name for the service')
    description = forms.CharField(max_length=200,
    	help_text=u'Enter a description',
    	widget=forms.Textarea)
    command = forms.CharField(max_length=200,
    	help_text=u'Enter a command you would type to run it')
    file = forms.FileField()


class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return u''
        return u'<div class="control-group error">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])

class ServiceStartForm(forms.Form):
    serviceList = service.models.Service.objects.all()
    print serviceList.count()
    b = {}
    for aService in serviceList:
        b[aService.id] = aService.name
    c = b.items()
    print "Within the form, ", serviceList.count()
    serviceChoice = forms.ChoiceField(choices=c, widget=forms.Select())
    input_directory = forms.CharField(max_length=200)
    output_directory = forms.CharField(max_length=200)