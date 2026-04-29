from rest_framework import serializers
from .models import Specialty, Qualification, Doctor


class SpecialtySerializer(serializers.ModelSerializer):
    doctors_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Specialty
        fields = ['id', 'name', 'description', 'doctors_count', 'created_at']
        read_only_fields = ['created_at']


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['id', 'name', 'price_multiplier', 'description']


class DoctorSerializer(serializers.ModelSerializer):
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)
    qualification_name = serializers.CharField(source='qualification.name', read_only=True)
    final_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Doctor
        fields = [
            'id', 'full_name',
            'specialty', 'specialty_name',
            'qualification', 'qualification_name',
            'consultation_price', 'final_price',
            'phone', 'is_active', 'hired_at',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class DoctorListSerializer(serializers.ModelSerializer):
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)
    qualification_name = serializers.CharField(source='qualification.name', read_only=True)
    final_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Doctor
        fields = [
            'id', 'full_name', 'specialty_name', 'qualification_name',
            'consultation_price', 'final_price', 'is_active',
        ]
