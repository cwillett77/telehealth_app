from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'user_type', 'specialization', 'credentials']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Custom logic to handle userType, specialization, and credentials
        return CustomUser.objects.create_user(**validated_data)
