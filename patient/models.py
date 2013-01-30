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

# Can be defined in properties.py
DISEASE_CHOICES = (
        ("CMF", "Cranio-Maxofacial"),
        ("BR", "Breast Reconstruction"),
        )

class Disease(models.Model):
    patient = models.ForeignKey(Patient)
    diseaseType = models.CharField(
        max_length=6, choices=DISEASE_CHOICES, default="CMF")

    def __unicode__(self):
        disease_hash = dict(DISEASE_CHOICES)
        return disease_hash[self.diseaseType]
