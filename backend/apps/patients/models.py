from datetime import date
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class DiscountCategory(models.Model):
    """Chegirma toifalari: Nafaqaxor, Faxriy, Bola va h.k."""

    name = models.CharField(
        'Nomi', max_length=50, unique=True
    )
    percent = models.DecimalField(
        'Foiz', max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    description = models.TextField('Tavsif', blank=True)
    is_active = models.BooleanField('Faolmi', default=True)
    created_at = models.DateTimeField('Yaratilgan', auto_now_add=True)

    class Meta:
        db_table = 'discount_category'
        verbose_name = 'Chegirma toifasi'
        verbose_name_plural = 'Chegirma toifalari'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.percent}%)'

    def calculate_discount(self, amount: Decimal) -> Decimal:
        """Berilgan summadan chegirma miqdorini hisoblaydi."""
        if not self.is_active:
            return Decimal('0')
        return (amount * self.percent / Decimal('100')).quantize(Decimal('0.01'))


class Patient(models.Model):
    """Bemorlar."""

    GENDER_CHOICES = [
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    ]

    full_name = models.CharField('F.I.O.', max_length=150)
    birth_date = models.DateField('Tug\'ilgan sana')
    gender = models.CharField('Jinsi', max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField('Telefon', max_length=20, unique=True)
    address = models.CharField('Manzil', max_length=255, blank=True)
    discount_category = models.ForeignKey(
        DiscountCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patients',
        verbose_name='Chegirma toifasi'
    )
    created_at = models.DateTimeField('Yaratilgan', auto_now_add=True)
    updated_at = models.DateTimeField('Yangilangan', auto_now=True)

    class Meta:
        db_table = 'patient'
        verbose_name = 'Bemor'
        verbose_name_plural = 'Bemorlar'
        ordering = ['full_name']
        indexes = [
            models.Index(fields=['full_name']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f'{self.full_name} ({self.phone})'

    @property
    def age(self) -> int:
        """Bemorning yoshini hisoblaydi."""
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
