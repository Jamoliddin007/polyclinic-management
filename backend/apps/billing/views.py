from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Payment


class PaymentViewSet(viewsets.ModelViewSet):
    """Placeholder — Bosqich 4'da to'liq implementatsiya."""
    queryset = Payment.objects.select_related('visit', 'visit__patient').all()
    permission_classes = [IsAuthenticated]
    serializer_class = None
