from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Visit, ProcedureType, VisitProcedure, VisitConsultation
from .serializers import (
    VisitSerializer, VisitListSerializer, VisitCreateSerializer,
    ProcedureTypeSerializer,
    VisitProcedureSerializer, VisitConsultationSerializer,
)


class ProcedureTypeViewSet(viewsets.ModelViewSet):
    queryset = ProcedureType.objects.all()
    serializer_class = ProcedureTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'base_price']


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.select_related(
        'patient', 'patient__discount_category',
        'primary_doctor', 'primary_doctor__specialty',
    ).prefetch_related('procedures__procedure_type', 'consultations__doctor').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['payment_status', 'visit_date', 'patient', 'primary_doctor']
    search_fields = ['patient__full_name', 'patient__phone', 'diagnosis']
    ordering_fields = ['visit_date', 'total_cost', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return VisitListSerializer
        if self.action == 'create':
            return VisitCreateSerializer
        return VisitSerializer

    @action(detail=True, methods=['post'])
    def recalculate(self, request, pk=None):
        """Murojaat summasini qayta hisoblash."""
        visit = self.get_object()
        visit.recalculate()
        return Response(VisitSerializer(visit).data)

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Murojaatni TO'LANGAN deb belgilash."""
        visit = self.get_object()
        visit.mark_as_paid()
        return Response({'status': visit.payment_status})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Murojaatni bekor qilish."""
        visit = self.get_object()
        visit.cancel()
        return Response({'status': visit.payment_status})


class VisitProcedureViewSet(viewsets.ModelViewSet):
    queryset = VisitProcedure.objects.select_related(
        'visit', 'procedure_type'
    ).all()
    serializer_class = VisitProcedureSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['visit', 'procedure_type']


class VisitConsultationViewSet(viewsets.ModelViewSet):
    queryset = VisitConsultation.objects.select_related('visit', 'doctor').all()
    serializer_class = VisitConsultationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['visit', 'doctor']
