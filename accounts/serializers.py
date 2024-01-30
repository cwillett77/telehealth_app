from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    # Define fields that are specific to doctors
    specialization = serializers.CharField(allow_blank=True, required=False)
    credentials = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'user_type', 'specialization', 'credentials']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Custom logic to handle userType, specialization, and credentials
        user_type = validated_data.get('user_type')

        # Remove specialization and credentials for patients
        if user_type == 'patient':
            validated_data.pop('specialization', None)
            validated_data.pop('credentials', None)

        return CustomUser.objects.create_user(**validated_data)
