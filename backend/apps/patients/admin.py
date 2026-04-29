from django.contrib import admin
from .models import DiscountCategory, Patient


@admin.register(DiscountCategory)
class DiscountCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'percent', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)
    list_editable = ('is_active',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'phone', 'gender', 'birth_date',
        'age', 'discount_category', 'created_at',
    )
    list_filter = ('gender', 'discount_category', 'created_at')
    search_fields = ('full_name', 'phone', 'address')
    autocomplete_fields = ('discount_category',)
    date_hierarchy = 'created_at'
    ordering = ('full_name',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('full_name', 'birth_date', 'gender')
        }),
        ('Aloqa', {
            'fields': ('phone', 'address')
        }),
        ('Chegirma', {
            'fields': ('discount_category',)
        }),
        ('Tizim', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Yoshi', ordering='birth_date')
    def age(self, obj):
        return obj.age
