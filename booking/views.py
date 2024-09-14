from accounts.models import CustomUser
from rest_framework import viewsets
from .models import Availability
from .serializers import AvailabilitySerializer
from rest_framework import status
from rest_framework.response import Response
from datetime import timedelta, datetime, timezone
from django.utils import timezone as dj_timezone
from django.utils import timezone as dj_timezone

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
            queryset = self.queryset.filter(doctor_id=doctor_id).order_by('start_time')
        else:
            queryset = self.queryset.order_by('start_time')

        # Convert datetime fields to local timezone before sending to serializer
        for availability in queryset:
            availability.start_time = dj_timezone.localtime(availability.start_time)
            availability.end_time = dj_timezone.localtime(availability.end_time)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
    def create(self, request):
        doctor_id = request.data.get('doctor')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        # Ensure the start_time and end_time strings are in the correct format
        if start_time.endswith('Z'):
            start_time = start_time[:-1]  # Remove the trailing 'Z'
        if end_time.endswith('Z'):
            end_time = end_time[:-1]  # Remove the trailing 'Z'

        # Parse the datetime strings and make them timezone-aware in UTC
        start_time = dj_timezone.make_aware(datetime.fromisoformat(start_time), timezone=timezone.utc)
        end_time = dj_timezone.make_aware(datetime.fromisoformat(end_time), timezone=timezone.utc)


        # Generate 30-minute time slots
        time_slots = generate_time_slots(start_time, end_time)

        # Create new availability records for each time slot
        for time_slot in time_slots:
            create_availability_record(
                doctor=CustomUser.objects.get(id=doctor_id),
                start_time=time_slot,
                end_time=time_slot + timedelta(minutes=30)
            )

        return Response({"message": "Availability created successfully"}, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk=None):
        doctor_id = request.query_params.get('doctor_id')
        
        if doctor_id is not None and pk is not None:
            availability = self.queryset.filter(doctor_id=doctor_id, pk=pk).first()
            if availability is not None:
                # Convert datetime fields to local timezone before sending to serializer
                availability.start_time = dj_timezone.localtime(availability.start_time)
                availability.end_time = dj_timezone.localtime(availability.end_time)

                serializer = self.get_serializer(availability)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, doctor_id, pk=None):
        # Retrieve the specific availability
        queryset = Availability.objects.filter(doctor_id=doctor_id, id=pk)
        
        if not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        availability = queryset.first()

        # Update the availability with the new data
        serializer = self.get_serializer(availability, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Delete conflicting availabilities
        Availability.objects.filter(
            doctor=availability.doctor,
            start_time__lt=availability.end_time,
            end_time__gt=availability.start_time,
            ).exclude(id=availability.id).delete()

        # Generate 30-minute time slots
        time_slots = generate_time_slots(availability.start_time, availability.end_time)
        
        # Delete the original availability
        availability.delete()
        
        # Create new availability records for each time slot
        for time_slot in time_slots:
            create_availability_record(
                doctor=availability.doctor,
                start_time=time_slot,
                end_time=time_slot + timedelta(minutes=30)
            )
        
        return Response(serializer.data)



    def destroy(self, request, doctor_id, pk=None):
        # Handle DELETE request for a specific availability item by doctor_id and availability_id
        queryset = Availability.objects.filter(doctor_id=doctor_id, id=pk)
        
        if not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        availability = queryset.first()
        availability.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
