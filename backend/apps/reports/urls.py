from django.urls import path
from .views import (
    DashboardKPIView,
    RevenueReportView,
    TopDoctorsView,
    SpecialtyDistributionView,
    DiscountDistributionView,
)
from .export_views import PatientHistoryPDFView, RevenueExcelView

urlpatterns = [
    path('dashboard/',              DashboardKPIView.as_view(),         name='dashboard-kpi'),
    path('revenue/',                RevenueReportView.as_view(),        name='report-revenue'),
    path('top-doctors/',            TopDoctorsView.as_view(),           name='report-top-doctors'),
    path('specialty-distribution/', SpecialtyDistributionView.as_view(), name='report-specialty'),
    path('discount-distribution/',  DiscountDistributionView.as_view(),  name='report-discount'),

    # Eksport
    path('export/patient-history/<int:patient_id>/', PatientHistoryPDFView.as_view(), name='export-patient-history'),
    path('export/revenue-excel/',                    RevenueExcelView.as_view(),       name='export-revenue-excel'),
]
