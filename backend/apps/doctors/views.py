from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Doctor, Specialty, Qualification
from .serializers import (
    DoctorSerializer, DoctorListSerializer,
    SpecialtySerializer, QualificationSerializer,
)


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.annotate(doctors_count=Count('doctors')).all()
    serializer_class = SpecialtySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'doctors_count']


class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name']


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('specialty', 'qualification').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['specialty', 'qualification', 'is_active']
    search_fields = ['full_name', 'phone']
    ordering_fields = ['full_name', 'consultation_price', 'hired_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorListSerializer
        return DoctorSerializer
