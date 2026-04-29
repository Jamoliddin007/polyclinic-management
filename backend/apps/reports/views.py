"""
Hisobot endpointlari — Bosqich 6'da to'liq implementatsiya.
Hozircha placeholder.
"""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class DashboardKPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'placeholder': 'Bosqich 6'})


class RevenueReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'placeholder': 'Bosqich 6'})


class TopDoctorsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'placeholder': 'Bosqich 6'})


class SpecialtyDistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'placeholder': 'Bosqich 6'})


class DiscountDistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'placeholder': 'Bosqich 6'})
