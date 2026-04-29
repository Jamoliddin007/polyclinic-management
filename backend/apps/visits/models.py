from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models

from apps.patients.models import Patient
from apps.doctors.models import Doctor


class ProcedureType(models.Model):
    """Tibbiy protseduralar lug'ati: UZI, qon tahlili, EKG..."""

    name = models.CharField('Nomi', max_length=150)
    base_price = models.DecimalField(
        'Asosiy narx', max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    duration_minutes = models.PositiveIntegerField('Davomiyligi (min)', default=15)
    description = models.TextField('Tavsif', blank=True)
    is_active = models.BooleanField('Faolmi', default=True)
    created_at = models.DateTimeField('Yaratilgan', auto_now_add=True)

    class Meta:
        db_table = 'procedure_type'
        verbose_name = 'Protsedura turi'
        verbose_name_plural = 'Protsedura turlari'
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f'{self.name} — {self.base_price:,.0f} so\'m'


class Visit(models.Model):
    """Bemor murojaati."""

    PAYMENT_STATUS_CHOICES = [
        ('PENDING',   'Kutilmoqda'),
        ('PAID',      'To\'langan'),
        ('CANCELLED', 'Bekor qilingan'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='visits',
        verbose_name='Bemor'
    )
    primary_doctor = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name='visits',
        verbose_name='Asosiy shifokor'
    )
    visit_date = models.DateField('Murojaat sanasi')
    diagnosis = models.TextField('Tashxis', blank=True)
    notes = models.TextField('Izohlar', blank=True)

    subtotal = models.DecimalField(
        'Chegirmagacha summa', max_digits=10, decimal_places=2,
        default=Decimal('0')
    )
    discount_amount = models.DecimalField(
        'Chegirma miqdori', max_digits=10, decimal_places=2,
        default=Decimal('0')
    )
    total_cost = models.DecimalField(
        'Yakuniy summa', max_digits=10, decimal_places=2,
        default=Decimal('0')
    )
    payment_status = models.CharField(
        'To\'lov holati', max_length=10,
        choices=PAYMENT_STATUS_CHOICES, default='PENDING'
    )

    created_at = models.DateTimeField('Yaratilgan', auto_now_add=True)
    updated_at = models.DateTimeField('Yangilangan', auto_now=True)

    class Meta:
        db_table = 'visit'
        verbose_name = 'Murojaat'
        verbose_name_plural = 'Murojaatlar'
        ordering = ['-visit_date', '-id']
        indexes = [
            models.Index(fields=['visit_date']),
            models.Index(fields=['patient']),
            models.Index(fields=['primary_doctor']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f'#{self.id} — {self.patient.full_name} ({self.visit_date})'

    def calculate_total_cost(self) -> Decimal:
        """Konsultatsiyalar + protseduralar yig'indisi (subtotal)."""
        from django.db.models import F, Sum

        primary_consultation = self.primary_doctor.final_price

        procedures_sum = self.procedures.aggregate(
            total=Sum(F('price_at_time') * F('quantity'))
        )['total'] or Decimal('0')

        consultations_sum = self.consultations.aggregate(
            total=Sum('price_at_time')
        )['total'] or Decimal('0')

        self.subtotal = primary_consultation + procedures_sum + consultations_sum
        return self.subtotal

    def apply_discount(self) -> Decimal:
        """Bemor chegirma toifasi bo'yicha chegirma qo'llaydi."""
        if self.patient.discount_category and self.patient.discount_category.is_active:
            self.discount_amount = self.patient.discount_category.calculate_discount(self.subtotal)
        else:
            self.discount_amount = Decimal('0')

        self.total_cost = self.subtotal - self.discount_amount
        return self.total_cost

    def recalculate(self, save: bool = True):
        """To'liq qayta hisoblash: subtotal + chegirma + total."""
        self.calculate_total_cost()
        self.apply_discount()
        if save:
            self.save(update_fields=['subtotal', 'discount_amount', 'total_cost', 'updated_at'])

    def mark_as_paid(self):
        self.payment_status = 'PAID'
        self.save(update_fields=['payment_status', 'updated_at'])

    def cancel(self):
        self.payment_status = 'CANCELLED'
        self.save(update_fields=['payment_status', 'updated_at'])


class VisitProcedure(models.Model):
    """Murojaatga biriktirilgan protsedura (M:N orali jadval)."""

    visit = models.ForeignKey(
        Visit, on_delete=models.CASCADE,
        related_name='procedures', verbose_name='Murojaat'
    )
    procedure_type = models.ForeignKey(
        ProcedureType, on_delete=models.PROTECT,
        related_name='visit_procedures', verbose_name='Protsedura'
    )
    price_at_time = models.DecimalField(
        'Shu paytdagi narxi', max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    quantity = models.PositiveIntegerField('Soni', default=1)
    notes = models.TextField('Izoh', blank=True)
    created_at = models.DateTimeField('Yaratilgan', auto_now_add=True)

    class Meta:
        db_table = 'visit_procedure'
        verbose_name = 'Murojaat protsedurasi'
        verbose_name_plural = 'Murojaat protseduralari'
        indexes = [
            models.Index(fields=['visit']),
            models.Index(fields=['procedure_type']),
        ]

    def __str__(self):
        return f'{self.procedure_type.name} × {self.quantity}'

    @property
    def subtotal(self) -> Decimal:
        return self.price_at_time * self.quantity

    def save(self, *args, **kwargs):
        if not self.price_at_time and self.procedure_type_id:
            self.price_at_time = self.procedure_type.base_price
        super().save(*args, **kwargs)


class VisitConsultation(models.Model):
    """Murojaat doirasidagi qo'shimcha shifokor konsultatsiyasi."""

    visit = models.ForeignKey(
        Visit, on_delete=models.CASCADE,
        related_name='consultations', verbose_name='Murojaat'
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.PROTECT,
        related_name='consultations', verbose_name='Shifokor'
    )
    price_at_time = models.DecimalField(
        'Shu paytdagi narxi', max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    notes = models.TextField('Izoh', blank=True)
    created_at = models.DateTimeField('Yaratilgan', auto_now_add=True)

    class Meta:
        db_table = 'visit_consultation'
        verbose_name = 'Konsultatsiya'
        verbose_name_plural = 'Konsultatsiyalar'
        indexes = [
            models.Index(fields=['visit']),
            models.Index(fields=['doctor']),
        ]

    def __str__(self):
        return f'{self.doctor.full_name} — {self.visit}'

    def save(self, *args, **kwargs):
        if not self.price_at_time and self.doctor_id:
            self.price_at_time = self.doctor.final_price
        super().save(*args, **kwargs)
