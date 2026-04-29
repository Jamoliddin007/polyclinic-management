from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from apps.visits.models import Visit


class Payment(models.Model):
    """Murojaat uchun to'lov yozuvi."""

    METHOD_CHOICES = [
        ('CASH',     'Naqd'),
        ('CARD',     'Karta'),
        ('TRANSFER', 'O\'tkazma'),
    ]

    visit = models.OneToOneField(
        Visit, on_delete=models.CASCADE,
        related_name='payment', verbose_name='Murojaat'
    )
    amount = models.DecimalField(
        'Summa', max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    method = models.CharField(
        'To\'lov usuli', max_length=10,
        choices=METHOD_CHOICES, default='CASH'
    )
    paid_at = models.DateTimeField('To\'langan vaqt', default=timezone.now)
    receipt_number = models.CharField(
        'Chek raqami', max_length=50, unique=True, blank=True
    )

    class Meta:
        db_table = 'payment'
        verbose_name = 'To\'lov'
        verbose_name_plural = 'To\'lovlar'
        ordering = ['-paid_at']
        indexes = [
            models.Index(fields=['paid_at']),
            models.Index(fields=['method']),
        ]

    def __str__(self):
        return f'#{self.receipt_number or self.id} — {self.amount:,.0f} so\'m'

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f'RCP-{timezone.now().year}-{self.visit_id:06d}'
        super().save(*args, **kwargs)

        if self.visit.payment_status != 'PAID':
            self.visit.mark_as_paid()
