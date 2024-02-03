from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .models import Availability

class AvailabilityTests(APITestCase):
    def setUp(self):
        # Create a doctor user
        self.user_model = get_user_model()
        self.doctor = self.user_model.objects.create_user(username='doctor', password='testpass123', user_type='doctor')
        self.client = APIClient()
        self.client.force_authenticate(user=self.doctor)  # Simulate doctor login

    def test_create_availability(self):
        """
        Ensure we can create a new availability slot.
        """
        url = reverse('availability-list')
        data = {'doctor': self.doctor.id, 'start_time': '2023-01-01T09:00:00Z', 'end_time': '2023-01-01T11:00:00Z'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Availability.objects.count(), 1)
        self.assertEqual(Availability.objects.get().doctor, self.doctor)

    def test_retrieve_availability_list(self):
        """
        Ensure we can retrieve a list of availabilities.
        """
        Availability.objects.create(doctor=self.doctor, start_time='2023-01-01T09:00:00Z', end_time='2023-01-01T11:00:00Z')
        url = reverse('availability-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming this is the only availability in the database
