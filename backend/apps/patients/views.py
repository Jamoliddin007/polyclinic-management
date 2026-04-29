from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Patient, DiscountCategory


class PatientViewSet(viewsets.ModelViewSet):
    """Placeholder — Bosqich 4'da to'liq implementatsiya."""
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = None  # set in Bosqich 4


class DiscountCategoryViewSet(viewsets.ModelViewSet):
    queryset = DiscountCategory.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = None  # set in Bosqich 4
