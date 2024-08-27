from rest_framework import viewsets
from .models import Availability
from .serializers import AvailabilitySerializer
from rest_framework import status
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone

def generate_time_slots(start_time, end_time):
    time_slots = []
    current_time = start_time
    while current_time < end_time:
        time_slots.append(current_time)
        current_time += timedelta(minutes=30)
    return time_slots

def create_availability_record(doctor, start_time, end_time):
    availability = Availability.objects.create(doctor=doctor, start_time=start_time, end_time=end_time)
    return availability

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    
    def list(self, request):
        doctor_id = request.query_params.get('doctor_id')
        if doctor_id is not None:
            queryset = self.queryset.filter(doctor_id=doctor_id)
        else:
            queryset = self.queryset

        # Convert datetime fields to local timezone before sending to serializer
        for availability in queryset:
            availability.start_time = timezone.localtime(availability.start_time)
            availability.end_time = timezone.localtime(availability.end_time)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        doctor_id = request.query_params.get('doctor_id')
        
        if doctor_id is not None and pk is not None:
            availability = self.queryset.filter(doctor_id=doctor_id, pk=pk).first()
            if availability is not None:
                # Convert datetime fields to local timezone before sending to serializer
                availability.start_time = timezone.localtime(availability.start_time)
                availability.end_time = timezone.localtime(availability.end_time)

                serializer = self.get_serializer(availability)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, doctor_id, pk=None):
        queryset = Availability.objects.filter(doctor_id=doctor_id, id=pk)
        
        if not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        availability = queryset.first()
        serializer = self.get_serializer(availability, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Generate 30-minute time slots
        time_slots = generate_time_slots(availability.start_time, availability.end_time)
        
        # Delete the original availability
        availability.delete()
        
        # Create new availability records for each time slot
        for time_slot in time_slots:
            create_availability_record(doctor=availability.doctor, start_time=time_slot, end_time=time_slot + timedelta(minutes=30))
            
        return Response(serializer.data)


    def destroy(self, request, doctor_id, pk=None):
        # Handle DELETE request for a specific availability item by doctor_id and availability_id
        queryset = Availability.objects.filter(doctor_id=doctor_id, id=pk)
        
        if not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        availability = queryset.first()
        availability.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
