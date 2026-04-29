from rest_framework import serializers
from .models import Visit, ProcedureType, VisitProcedure, VisitConsultation


class ProcedureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureType
        fields = [
            'id', 'name', 'base_price', 'duration_minutes',
            'description', 'is_active', 'created_at',
        ]
        read_only_fields = ['created_at']


class VisitProcedureSerializer(serializers.ModelSerializer):
    procedure_name = serializers.CharField(source='procedure_type.name', read_only=True)
    subtotal = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = VisitProcedure
        fields = [
            'id', 'visit', 'procedure_type', 'procedure_name',
            'price_at_time', 'quantity', 'notes', 'subtotal', 'created_at',
        ]
        read_only_fields = ['created_at']
        extra_kwargs = {
            'price_at_time': {'required': False, 'allow_null': True},
        }


class VisitProcedureNestedSerializer(serializers.ModelSerializer):
    """Visit ichida nested holatda foydalanish uchun."""
    procedure_name = serializers.CharField(source='procedure_type.name', read_only=True)
    subtotal = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = VisitProcedure
        fields = [
            'id', 'procedure_type', 'procedure_name',
            'price_at_time', 'quantity', 'notes', 'subtotal',
        ]


class VisitConsultationSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)

    class Meta:
        model = VisitConsultation
        fields = [
            'id', 'visit', 'doctor', 'doctor_name',
            'price_at_time', 'notes', 'created_at',
        ]
        read_only_fields = ['created_at']
        extra_kwargs = {
            'price_at_time': {'required': False, 'allow_null': True},
        }


class VisitConsultationNestedSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)

    class Meta:
        model = VisitConsultation
        fields = ['id', 'doctor', 'doctor_name', 'price_at_time', 'notes']


class VisitSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='primary_doctor.full_name', read_only=True)
    procedures = VisitProcedureNestedSerializer(many=True, read_only=True)
    consultations = VisitConsultationNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Visit
        fields = [
            'id', 'patient', 'patient_name',
            'primary_doctor', 'doctor_name',
            'visit_date', 'diagnosis', 'notes',
            'subtotal', 'discount_amount', 'total_cost', 'payment_status',
            'procedures', 'consultations',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'subtotal', 'discount_amount', 'total_cost',
            'created_at', 'updated_at',
        ]


class VisitListSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='primary_doctor.full_name', read_only=True)
    specialty_name = serializers.CharField(
        source='primary_doctor.specialty.name', read_only=True
    )

    class Meta:
        model = Visit
        fields = [
            'id', 'patient_name', 'doctor_name', 'specialty_name',
            'visit_date', 'total_cost', 'payment_status',
        ]


class VisitCreateSerializer(serializers.ModelSerializer):
    """Yangi murojaat yaratish — protseduralar va konsultatsiyalar bilan."""
    procedures = VisitProcedureNestedSerializer(many=True, required=False)
    consultations = VisitConsultationNestedSerializer(many=True, required=False)

    class Meta:
        model = Visit
        fields = [
            'id', 'patient', 'primary_doctor', 'visit_date',
            'diagnosis', 'notes', 'procedures', 'consultations',
        ]

    def create(self, validated_data):
        procedures_data = validated_data.pop('procedures', [])
        consultations_data = validated_data.pop('consultations', [])

        visit = Visit.objects.create(**validated_data)

        for proc in procedures_data:
            VisitProcedure.objects.create(visit=visit, **proc)
        for cons in consultations_data:
            VisitConsultation.objects.create(visit=visit, **cons)

        visit.refresh_from_db()
        return visit
