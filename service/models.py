from django.db import models

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=400)
    command = models.CharField(max_length=400)

    def __unicode__(self):
        return self.name


class ServiceRun(models.Model):
    SERVICE_STATUS_CHOICES = (
        ("STOPPED", "Stopped"),
        ("RUNNING", "Running"),
        ("COMPLETED", "Completed"),
        ("READY", "Ready"),
    )
    service = models.ForeignKey(Service)
    status = models.CharField(
        max_length=10, choices=SERVICE_STATUS_CHOICES, default="READY")
    inputParams = models.CharField(max_length=500)
    outputParams = models.CharField(max_length=500)
    pid = models.IntegerField(default=-1)

    def is_running(self):
        return self.status == RUNNING

    def __unicode__(self):
    	return self.service.name
