from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Doctor, Specialty, Qualification


class DoctorViewSet(viewsets.ModelViewSet):
    """Placeholder — Bosqich 4'da to'liq implementatsiya."""
    queryset = Doctor.objects.select_related('specialty', 'qualification').all()
    permission_classes = [IsAuthenticated]
    serializer_class = None


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = None


class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = None
