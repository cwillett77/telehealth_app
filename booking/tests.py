from django.urls import reverse
from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Doctor, Patient, Appointment 
from django.contrib.auth.models import User


class AppointmentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.force_authenticate(user=self.user)
        
        # Create test data
        self.doctor = Doctor.objects.create(name="Dr. Smith", specialization="Cardiology")
        self.patient = Patient.objects.create(name="John Doe", date_of_birth="1980-01-01")
        
        self.appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_time=datetime(2024, 1, 1, 9, 0),
            status='scheduled'
        )

    def test_create_appointment(self):
        url = reverse('appointment-list')
        data = {
            'doctor': self.doctor.id,  # Assuming self.doctor is created in setUp
            'patient': self.patient.id,  # Assuming self.patient is created in setUp
            'appointment_time': '2024-01-01T09:00',
            'status': 'scheduled'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_appointments(self):
        # Test listing appointments
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Adjust based on expected data


