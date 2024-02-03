from django.db import models
from accounts.models import CustomUser

class Availability(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='availabilities', limit_choices_to={'user_type': 'doctor'})
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.doctor.username} available from {self.start_time} to {self.end_time}"
