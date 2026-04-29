from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Patient, DiscountCategory
from .serializers import (
    PatientSerializer, PatientListSerializer, DiscountCategorySerializer,
)


class DiscountCategoryViewSet(viewsets.ModelViewSet):
    queryset = DiscountCategory.objects.all()
    serializer_class = DiscountCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'percent']


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related('discount_category').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['gender', 'discount_category']
    search_fields = ['full_name', 'phone', 'address']
    ordering_fields = ['full_name', 'birth_date', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        return PatientSerializer
