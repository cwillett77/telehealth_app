# models.py
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class Availability(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='availabilities', limit_choices_to={'user_type': 'doctor'})
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Ensure start_time and end_time are in UTC timezone before saving
        if self.start_time.tzinfo is None or self.start_time.tzinfo.utcoffset(self.start_time) is None:
            self.start_time = timezone.make_aware(self.start_time, timezone.utc)
        if self.end_time.tzinfo is None or self.end_time.tzinfo.utcoffset(self.end_time) is None:
            self.end_time = timezone.make_aware(self.end_time, timezone.utc)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doctor.username} available from {self.start_time} to {self.end_time}"

class Appointment(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to={'user_type': 'doctor'})
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointments', limit_choices_to={'user_type': 'patient'})
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=(('booked', 'Booked'), ('completed', 'Completed'), ('cancelled', 'Cancelled')))

    def __str__(self):
        return f"Appointment with {self.doctor.username} for {self.patient.username} at {self.appointment_time}"
