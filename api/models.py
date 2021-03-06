from django.db import models
from datetime import datetime
from django.utils import timezone


class User(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    userType = models.CharField(max_length=20)
    birthDate = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    weight = models.IntegerField()
    height = models.IntegerField()
    xp = models.IntegerField(blank=True, default=0)


class PatientMeasures(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    glycemia = models.FloatField(blank=True, default=None, null=True)
    ldl = models.FloatField(blank=True, default=None, null=True)
    hdl = models.FloatField(blank=True, default=None, null=True)
    trygliceride = models.FloatField(blank=True, default=None, null=True)
    bloodPressure = models.FloatField(blank=True, default=None, null=True)
    weight = models.IntegerField(blank=True, default=None, null=True)
    heartbeat = models.IntegerField(blank=True, default=None, null=True)
    timestamp = models.CharField(max_length=100)


class ExamType(models.Model):
    examType = models.CharField(max_length=250)


class Measures(models.Model):
    value = models.FloatField(blank=True, default=None, null=True)
    measuredQuantity = models.CharField(max_length=100)
    examType = models.ForeignKey(ExamType, on_delete=models.CASCADE)


class ExamReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.CharField(max_length=100)
    measures = models.ManyToManyField(Measures)


class DiseaseRisk(models.Model):
    diseaseName = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
