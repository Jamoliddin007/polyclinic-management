from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


class Specialty(models.Model):
    """Mutaxassisliklar: kardiologiya, terapiya, stomatologiya..."""

    name = models.CharField('Nomi', max_length=100, unique=True)
    description = models.TextField('Tavsif', blank=True)
    created_at = models.DateTimeField('Yaratilgan', auto_now_add=True)

    class Meta:
        db_table = 'specialty'
        verbose_name = 'Mutaxassislik'
        verbose_name_plural = 'Mutaxassisliklar'
        ordering = ['name']

    def __str__(self):
        return self.name


class Qualification(models.Model):
    """Shifokor malaka darajasi: Stajor, Birinchi toifa, Oliy toifa..."""

    name = models.CharField('Nomi', max_length=50, unique=True)
    price_multiplier = models.DecimalField(
        'Narx koeffitsienti', max_digits=4, decimal_places=2,
        default=Decimal('1.00'),
        validators=[MinValueValidator(Decimal('0'))]
    )
    description = models.TextField('Tavsif', blank=True)

    class Meta:
        db_table = 'qualification'
        verbose_name = 'Malaka darajasi'
        verbose_name_plural = 'Malaka darajalari'
        ordering = ['price_multiplier']

    def __str__(self):
        return f'{self.name} (×{self.price_multiplier})'


class Doctor(models.Model):
    """Shifokorlar."""

    full_name = models.CharField('F.I.O.', max_length=150)
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        related_name='doctors',
        verbose_name='Mutaxassislik'
    )
    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.PROTECT,
        related_name='doctors',
        verbose_name='Malaka'
    )
    consultation_price = models.DecimalField(
        'Konsultatsiya narxi', max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    phone = models.CharField('Telefon', max_length=20, blank=True)
    is_active = models.BooleanField('Faolmi', default=True)
    hired_at = models.DateField('Ishga kirgan sana', null=True, blank=True)
    created_at = models.DateTimeField('Yaratilgan', auto_now_add=True)
    updated_at = models.DateTimeField('Yangilangan', auto_now=True)

    class Meta:
        db_table = 'doctor'
        verbose_name = 'Shifokor'
        verbose_name_plural = 'Shifokorlar'
        ordering = ['full_name']
        indexes = [
            models.Index(fields=['specialty']),
            models.Index(fields=['is_active']),
            models.Index(fields=['full_name']),
        ]

    def __str__(self):
        return f'{self.full_name} — {self.specialty.name}'

    @property
    def final_price(self) -> Decimal:
        """Malaka koeffitsienti bilan yakuniy narx."""
        return (self.consultation_price * self.qualification.price_multiplier).quantize(Decimal('0.01'))
