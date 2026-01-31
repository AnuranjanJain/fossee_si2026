"""
Serializers for Chemical Equipment Parameter Visualizer.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Equipment, UploadSession


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for Equipment model."""
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class UploadSessionSerializer(serializers.ModelSerializer):
    """Serializer for UploadSession model."""
    equipment_count = serializers.IntegerField(source='record_count', read_only=True)
    summary = serializers.SerializerMethodField()
    
    class Meta:
        model = UploadSession
        fields = ['id', 'filename', 'uploaded_at', 'equipment_count', 'summary']
    
    def get_summary(self, obj):
        return obj.summary


class SummarySerializer(serializers.Serializer):
    """Serializer for summary statistics."""
    total_count = serializers.IntegerField()
    avg_flowrate = serializers.FloatField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    min_flowrate = serializers.FloatField()
    max_flowrate = serializers.FloatField()
    min_pressure = serializers.FloatField()
    max_pressure = serializers.FloatField()
    min_temperature = serializers.FloatField()
    max_temperature = serializers.FloatField()
    type_distribution = serializers.DictField()


class LoginSerializer(serializers.Serializer):
    """Serializer for login credentials."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration."""
    username = serializers.CharField(min_length=3, max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

