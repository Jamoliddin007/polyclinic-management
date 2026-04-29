from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source='visit.patient.full_name', read_only=True
    )
    visit_date = serializers.DateField(source='visit.visit_date', read_only=True)
    method_display = serializers.CharField(source='get_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'visit', 'patient_name', 'visit_date',
            'amount', 'method', 'method_display',
            'paid_at', 'receipt_number',
        ]
        read_only_fields = ['receipt_number']
