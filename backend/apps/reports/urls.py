from django.urls import path
from .views import (
    DashboardKPIView,
    RevenueReportView,
    TopDoctorsView,
    SpecialtyDistributionView,
    DiscountDistributionView,
)

urlpatterns = [
    path('dashboard/',              DashboardKPIView.as_view(),         name='dashboard-kpi'),
    path('revenue/',                RevenueReportView.as_view(),        name='report-revenue'),
    path('top-doctors/',            TopDoctorsView.as_view(),           name='report-top-doctors'),
    path('specialty-distribution/', SpecialtyDistributionView.as_view(), name='report-specialty'),
    path('discount-distribution/',  DiscountDistributionView.as_view(),  name='report-discount'),
]
