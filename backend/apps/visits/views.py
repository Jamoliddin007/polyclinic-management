from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Visit, ProcedureType, VisitProcedure, VisitConsultation


class VisitViewSet(viewsets.ModelViewSet):
    """Placeholder — Bosqich 4'da to'liq implementatsiya."""
    queryset = Visit.objects.select_related('patient', 'primary_doctor').all()
    permission_classes = [IsAuthenticated]
    serializer_class = None


class ProcedureTypeViewSet(viewsets.ModelViewSet):
    queryset = ProcedureType.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = None


class VisitProcedureViewSet(viewsets.ModelViewSet):
    queryset = VisitProcedure.objects.select_related('visit', 'procedure_type').all()
    permission_classes = [IsAuthenticated]
    serializer_class = None


class VisitConsultationViewSet(viewsets.ModelViewSet):
    queryset = VisitConsultation.objects.select_related('visit', 'doctor').all()
    permission_classes = [IsAuthenticated]
    serializer_class = None
