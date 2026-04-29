from django.contrib import admin
from .models import ProcedureType, Visit, VisitProcedure, VisitConsultation


@admin.register(ProcedureType)
class ProcedureTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'base_price', 'duration_minutes', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    ordering = ('name',)


class VisitProcedureInline(admin.TabularInline):
    model = VisitProcedure
    extra = 1
    autocomplete_fields = ('procedure_type',)
    fields = ('procedure_type', 'price_at_time', 'quantity', 'notes')


class VisitConsultationInline(admin.TabularInline):
    model = VisitConsultation
    extra = 0
    autocomplete_fields = ('doctor',)
    fields = ('doctor', 'price_at_time', 'notes')


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'patient', 'primary_doctor', 'visit_date',
        'subtotal', 'discount_amount', 'total_cost', 'payment_status',
    )
    list_filter = ('payment_status', 'visit_date', 'primary_doctor__specialty')
    search_fields = (
        'patient__full_name', 'patient__phone',
        'primary_doctor__full_name', 'diagnosis',
    )
    autocomplete_fields = ('patient', 'primary_doctor')
    date_hierarchy = 'visit_date'
    readonly_fields = ('subtotal', 'discount_amount', 'total_cost', 'created_at', 'updated_at')
    inlines = [VisitProcedureInline, VisitConsultationInline]

    fieldsets = (
        ('Asosiy', {
            'fields': ('patient', 'primary_doctor', 'visit_date')
        }),
        ('Klinik', {
            'fields': ('diagnosis', 'notes')
        }),
        ('To\'lov', {
            'fields': ('subtotal', 'discount_amount', 'total_cost', 'payment_status')
        }),
        ('Tizim', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_paid', 'recalculate_totals']

    @admin.action(description='Belgilangan murojaatlarni TO\'LANGAN deb belgilash')
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(payment_status='PAID')
        self.message_user(request, f'{updated} ta murojaat to\'langan deb belgilandi.')

    @admin.action(description='Summalarni qayta hisoblash')
    def recalculate_totals(self, request, queryset):
        for visit in queryset:
            visit.recalculate()
        self.message_user(request, f'{queryset.count()} ta murojaat qayta hisoblandi.')


@admin.register(VisitProcedure)
class VisitProcedureAdmin(admin.ModelAdmin):
    list_display = ('id', 'visit', 'procedure_type', 'price_at_time', 'quantity', 'subtotal')
    search_fields = ('visit__patient__full_name', 'procedure_type__name')
    autocomplete_fields = ('visit', 'procedure_type')


@admin.register(VisitConsultation)
class VisitConsultationAdmin(admin.ModelAdmin):
    list_display = ('id', 'visit', 'doctor', 'price_at_time')
    search_fields = ('visit__patient__full_name', 'doctor__full_name')
    autocomplete_fields = ('visit', 'doctor')
