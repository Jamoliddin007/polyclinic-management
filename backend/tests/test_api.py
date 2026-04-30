import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser('admin', 'admin@x.com', 'admin12345')


@pytest.fixture
def auth_client(admin_user):
    client = APIClient()
    response = client.post('/api/auth/login/', {
        'username': 'admin', 'password': 'admin12345',
    }, format='json')
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.mark.django_db
class TestAuth:
    def test_login_returns_tokens(self, admin_user):
        client = APIClient()
        response = client.post('/api/auth/login/', {
            'username': 'admin', 'password': 'admin12345',
        }, format='json')
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_unauthenticated_blocked(self):
        client = APIClient()
        response = client.get('/api/patients/patients/')
        assert response.status_code == 401


@pytest.mark.django_db
class TestPatientsAPI:
    def test_list(self, auth_client, patient):
        response = auth_client.get('/api/patients/patients/')
        assert response.status_code == 200
        assert response.data['count'] == 1

    def test_create(self, auth_client, discount_category):
        response = auth_client.post('/api/patients/patients/', {
            'full_name': 'Yangi Bemor',
            'birth_date': '1990-01-01',
            'gender': 'F',
            'phone': '+998901111111',
            'discount_category': discount_category.id,
        }, format='json')
        assert response.status_code == 201

    def test_search(self, auth_client, patient):
        response = auth_client.get(f'/api/patients/patients/?search={patient.full_name[:4]}')
        assert response.status_code == 200
        assert response.data['count'] >= 1


@pytest.mark.django_db
class TestVisitsAPI:
    def test_create_with_procedures(self, auth_client, patient, doctor, procedure_type):
        response = auth_client.post('/api/visits/visits/', {
            'patient': patient.id,
            'primary_doctor': doctor.id,
            'visit_date': '2026-04-30',
            'diagnosis': 'Test',
            'procedures': [
                {'procedure_type': procedure_type.id, 'quantity': 2},
            ],
        }, format='json')
        assert response.status_code == 201
        assert response.data['id']

    def test_recalculate_action(self, auth_client, visit):
        response = auth_client.post(f'/api/visits/visits/{visit.id}/recalculate/')
        assert response.status_code == 200

    def test_mark_paid_action(self, auth_client, visit):
        response = auth_client.post(f'/api/visits/visits/{visit.id}/mark_paid/')
        assert response.status_code == 200
        assert response.data['status'] == 'PAID'


@pytest.mark.django_db
class TestReportsAPI:
    def test_dashboard_kpi(self, auth_client):
        response = auth_client.get('/api/reports/dashboard/')
        assert response.status_code == 200
        assert 'patients_total' in response.data
        assert 'revenue_total' in response.data
