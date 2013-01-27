from django.db import models

# Create your models here.


class Patient(models.Model):
    name = models.CharField(max_length=200)
    dateOfBirth = models.DateTimeField("date of birth")
    identification = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=50)
    ethnicity = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)

    def __unicode__(self):
        return self.name
