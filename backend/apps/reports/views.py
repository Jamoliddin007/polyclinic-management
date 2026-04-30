"""
Hisobot endpointlari + PDF/Excel eksport.
"""
from datetime import date, timedelta
from io import BytesIO

from django.db.models import Count, Sum, Q, F
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.patients.models import Patient, DiscountCategory
from apps.doctors.models import Doctor, Specialty
from apps.visits.models import Visit


class DashboardKPIView(APIView):
    """Bosh ekran uchun asosiy ko'rsatkichlar."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        month_start = today.replace(day=1)

        paid = Visit.objects.filter(payment_status='PAID')

        return Response({
            'patients_total':   Patient.objects.count(),
            'doctors_total':    Doctor.objects.filter(is_active=True).count(),
            'visits_total':     Visit.objects.count(),
            'visits_today':     Visit.objects.filter(visit_date=today).count(),
            'visits_pending':   Visit.objects.filter(payment_status='PENDING').count(),

            'revenue_today':    paid.filter(visit_date=today).aggregate(s=Sum('total_cost'))['s'] or 0,
            'revenue_month':    paid.filter(visit_date__gte=month_start).aggregate(s=Sum('total_cost'))['s'] or 0,
            'revenue_total':    paid.aggregate(s=Sum('total_cost'))['s'] or 0,

            'discount_given_total':
                paid.aggregate(s=Sum('discount_amount'))['s'] or 0,
        })


class RevenueReportView(APIView):
    """Oxirgi 30 kunlik kunlik daromad."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        end = timezone.now().date()
        start = end - timedelta(days=days)

        rows = (
            Visit.objects
            .filter(payment_status='PAID', visit_date__gte=start, visit_date__lte=end)
            .values('visit_date')
            .annotate(
                visit_count=Count('id'),
                gross=Sum('subtotal'),
                discount=Sum('discount_amount'),
                net=Sum('total_cost'),
            )
            .order_by('visit_date')
        )

        return Response({
            'period': {'start': start, 'end': end},
            'data': list(rows),
        })


class TopDoctorsView(APIView):
    """Eng faol shifokorlar (murojaatlar va daromad bo'yicha)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get('limit', 10))

        rows = (
            Doctor.objects
            .annotate(
                total_visits=Count('visits', filter=Q(visits__payment_status='PAID')),
                total_revenue=Sum('visits__total_cost', filter=Q(visits__payment_status='PAID')),
            )
            .filter(total_visits__gt=0)
            .order_by('-total_visits')[:limit]
            .values('id', 'full_name', 'specialty__name', 'total_visits', 'total_revenue')
        )

        return Response(list(rows))


class SpecialtyDistributionView(APIView):
    """Mutaxassislik bo'yicha murojaatlar taqsimoti."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rows = (
            Specialty.objects
            .annotate(
                visit_count=Count(
                    'doctors__visits',
                    filter=Q(doctors__visits__payment_status='PAID'),
                ),
                revenue=Sum(
                    'doctors__visits__total_cost',
                    filter=Q(doctors__visits__payment_status='PAID'),
                ),
            )
            .order_by('-visit_count')
            .values('id', 'name', 'visit_count', 'revenue')
        )

        return Response(list(rows))


class DiscountDistributionView(APIView):
    """Chegirma toifalari bo'yicha bemorlar va daromad."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rows = (
            DiscountCategory.objects
            .annotate(
                patients_count=Count('patients', distinct=True),
                visits_count=Count(
                    'patients__visits',
                    filter=Q(patients__visits__payment_status='PAID'),
                    distinct=True,
                ),
                discount_given=Sum(
                    'patients__visits__discount_amount',
                    filter=Q(patients__visits__payment_status='PAID'),
                ),
            )
            .values('id', 'name', 'percent', 'patients_count', 'visits_count', 'discount_given')
        )

        return Response(list(rows))
