import pytest
from decimal import Decimal
from datetime import date


@pytest.fixture
def discount_category(db):
    from apps.patients.models import DiscountCategory
    return DiscountCategory.objects.create(
        name='Nafaqaxor', percent=Decimal('15.00'),
    )


@pytest.fixture
def patient(db, discount_category):
    from apps.patients.models import Patient
    return Patient.objects.create(
        full_name='Test Bemor',
        birth_date=date(1980, 1, 1),
        gender='M',
        phone='+998901234567',
        discount_category=discount_category,
    )


@pytest.fixture
def specialty(db):
    from apps.doctors.models import Specialty
    return Specialty.objects.create(name='Terapiya')


@pytest.fixture
def qualification(db):
    from apps.doctors.models import Qualification
    return Qualification.objects.create(
        name='Oliy toifa', price_multiplier=Decimal('1.5')
    )


@pytest.fixture
def doctor(db, specialty, qualification):
    from apps.doctors.models import Doctor
    return Doctor.objects.create(
        full_name='Dr. Test',
        specialty=specialty,
        qualification=qualification,
        consultation_price=Decimal('100000.00'),
    )


@pytest.fixture
def procedure_type(db):
    from apps.visits.models import ProcedureType
    return ProcedureType.objects.create(
        name='Qon tahlili',
        base_price=Decimal('50000.00'),
    )


@pytest.fixture
def visit(db, patient, doctor):
    from apps.visits.models import Visit
    return Visit.objects.create(
        patient=patient,
        primary_doctor=doctor,
        visit_date=date.today(),
    )
