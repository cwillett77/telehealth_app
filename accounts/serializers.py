from rest_framework import serializers
from .models import CustomUser

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'specialization', 'credentials')

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'user_type', 'specialization', 'credentials')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_type = validated_data.get('user_type')
        if user_type == 'doctor':
            # Validate doctor-specific fields here if necessary
            pass
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def validate(self, data):
        user_type = data.get('user_type')
        if user_type == 'doctor' and (not data.get('specialization') or not data.get('credentials')):
            raise serializers.ValidationError("Doctors must provide specialization and credentials.")
        return data
