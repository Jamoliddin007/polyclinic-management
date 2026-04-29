from rest_framework import serializers
from .models import DiscountCategory, Patient


class DiscountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCategory
        fields = ['id', 'name', 'percent', 'description', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)
    discount_category_name = serializers.CharField(
        source='discount_category.name', read_only=True
    )
    discount_percent = serializers.DecimalField(
        source='discount_category.percent', read_only=True,
        max_digits=5, decimal_places=2,
    )

    class Meta:
        model = Patient
        fields = [
            'id', 'full_name', 'birth_date', 'age', 'gender',
            'phone', 'address',
            'discount_category', 'discount_category_name', 'discount_percent',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class PatientListSerializer(serializers.ModelSerializer):
    """Yengilroq versiya — ro'yxat uchun."""
    age = serializers.IntegerField(read_only=True)
    discount_category_name = serializers.CharField(
        source='discount_category.name', read_only=True, default=None
    )

    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'phone', 'age', 'gender', 'discount_category_name']
