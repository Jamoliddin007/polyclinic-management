from django.contrib import admin
from .models import Specialty, Qualification, Doctor


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price_multiplier')
    search_fields = ('name',)
    ordering = ('price_multiplier',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'specialty', 'qualification',
        'consultation_price', 'final_price', 'is_active', 'phone',
    )
    list_filter = ('specialty', 'qualification', 'is_active')
    search_fields = ('full_name', 'phone')
    autocomplete_fields = ('specialty', 'qualification')
    list_editable = ('is_active',)
    ordering = ('full_name',)

    fieldsets = (
        ('Asosiy', {
            'fields': ('full_name', 'specialty', 'qualification')
        }),
        ('Narx va aloqa', {
            'fields': ('consultation_price', 'phone')
        }),
        ('Holat', {
            'fields': ('is_active', 'hired_at')
        }),
    )

    @admin.display(description='Yakuniy narx')
    def final_price(self, obj):
        return obj.final_price
