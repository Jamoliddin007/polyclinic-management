from decimal import Decimal
from datetime import date
import pytest


@pytest.mark.django_db
class TestDiscountCategory:
    def test_calculate_discount(self, discount_category):
        result = discount_category.calculate_discount(Decimal('100000'))
        assert result == Decimal('15000.00')

    def test_inactive_returns_zero(self, discount_category):
        discount_category.is_active = False
        discount_category.save()
        assert discount_category.calculate_discount(Decimal('100000')) == Decimal('0')


@pytest.mark.django_db
class TestPatient:
    def test_age_calculation(self, patient):
        # patient born 1980-01-01
        expected = date.today().year - 1980 - (
            (date.today().month, date.today().day) < (1, 1)
        )
        assert patient.age == expected

    def test_str_includes_phone(self, patient):
        assert patient.phone in str(patient)


@pytest.mark.django_db
class TestDoctor:
    def test_final_price_with_multiplier(self, doctor):
        # consultation 100000, multiplier 1.5 → 150000
        assert doctor.final_price == Decimal('150000.00')


@pytest.mark.django_db
class TestVisitBusinessLogic:
    def test_subtotal_zero_initially(self, visit):
        assert visit.subtotal == Decimal('0')

    def test_calculate_with_only_consultation(self, visit, doctor):
        visit.calculate_total_cost()
        assert visit.subtotal == doctor.final_price  # 150000

    def test_apply_discount(self, visit):
        # patient has 15% discount, consultation 150000
        visit.calculate_total_cost()
        visit.apply_discount()
        assert visit.discount_amount == Decimal('22500.00')
        assert visit.total_cost == Decimal('127500.00')

    def test_signal_recalculates_on_procedure_add(self, visit, procedure_type):
        from apps.visits.models import VisitProcedure
        VisitProcedure.objects.create(
            visit=visit, procedure_type=procedure_type, quantity=2,
        )
        visit.refresh_from_db()
        # consultation 150000 + 2 × 50000 = 250000
        assert visit.subtotal == Decimal('250000.00')
        # 15% discount = 37500
        assert visit.discount_amount == Decimal('37500.00')
        assert visit.total_cost == Decimal('212500.00')

    def test_mark_as_paid(self, visit):
        visit.mark_as_paid()
        assert visit.payment_status == 'PAID'


@pytest.mark.django_db
class TestVisitProcedure:
    def test_auto_price_from_procedure_type(self, visit, procedure_type):
        from apps.visits.models import VisitProcedure
        vp = VisitProcedure.objects.create(
            visit=visit, procedure_type=procedure_type,
        )
        assert vp.price_at_time == procedure_type.base_price

    def test_subtotal_calculation(self, visit, procedure_type):
        from apps.visits.models import VisitProcedure
        vp = VisitProcedure.objects.create(
            visit=visit, procedure_type=procedure_type, quantity=3,
        )
        assert vp.subtotal == Decimal('150000.00')


@pytest.mark.django_db
class TestPayment:
    def test_payment_marks_visit_paid(self, visit):
        from apps.billing.models import Payment
        Payment.objects.create(visit=visit, amount=Decimal('100000'))
        visit.refresh_from_db()
        assert visit.payment_status == 'PAID'

    def test_receipt_number_auto_generated(self, visit):
        from apps.billing.models import Payment
        payment = Payment.objects.create(visit=visit, amount=Decimal('100000'))
        assert payment.receipt_number.startswith('RCP-')
        assert str(visit.id).zfill(6) in payment.receipt_number
