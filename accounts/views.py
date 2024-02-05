from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer, DoctorSerializer

class DoctorListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.filter(user_type="doctor")
    serializer_class = DoctorSerializer
    
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, "username": username, "id": user.id, "user_type": user.user_type}, status=200)
    return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['POST'])
def logout(request):
    request.auth.delete()
    return Response(status=204)
