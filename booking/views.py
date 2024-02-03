from rest_framework import viewsets
from .models import Availability
from .serializers import AvailabilitySerializer

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

    def get_queryset(self):
        """
        Optionally restricts the returned availabilities to a given doctor,
        by filtering against a 'doctor' query parameter in the URL.
        """
        queryset = self.queryset
        doctor_id = self.request.query_params.get('doctor')
        if doctor_id is not None:
            queryset = queryset.filter(doctor_id=doctor_id)
        return queryset
