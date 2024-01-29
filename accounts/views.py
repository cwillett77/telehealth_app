from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import Doctor, Patient


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        user_type = serializer.validated_data.get('user_type')

        if user_type == 'doctor':
            Doctor.objects.create(user=user, specialization=serializer.validated_data.get('specialization'), credentials=serializer.validated_data.get('credentials'))
        elif user_type == 'patient':
            Patient.objects.create(user=user)

        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=200)
    return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['POST'])
def logout(request):
    request.auth.delete()
    return Response(status=204)
