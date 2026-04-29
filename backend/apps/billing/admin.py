from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'receipt_number', 'visit', 'amount', 'method', 'paid_at')
    list_filter = ('method', 'paid_at')
    search_fields = ('receipt_number', 'visit__patient__full_name')
    autocomplete_fields = ('visit',)
    date_hierarchy = 'paid_at'
    readonly_fields = ('receipt_number',)
