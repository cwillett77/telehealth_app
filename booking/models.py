from django.db import models
from accounts.models import CustomUser

class Availability(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='availabilities', limit_choices_to={'user_type': 'doctor'})
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.doctor.username} available from {self.start_time} to {self.end_time}"

class Appointment(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to={'user_type': 'doctor'})
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointments', limit_choices_to={'user_type': 'patient'})
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=(('booked', 'Booked'), ('completed', 'Completed'), ('cancelled', 'Cancelled')))

    def __str__(self):
        return f"Appointment with {self.doctor.username} for {self.patient.username} at {self.appointment_time}"
