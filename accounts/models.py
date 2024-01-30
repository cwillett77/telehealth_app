# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('doctor', 'Doctor'), 
        ('patient', 'Patient')
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.TextField()
    credentials = models.TextField()

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add patient-specific fields here if needed
