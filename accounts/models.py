from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('doctor', 'Doctor'), 
        ('patient', 'Patient')
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    credentials = models.TextField()

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
