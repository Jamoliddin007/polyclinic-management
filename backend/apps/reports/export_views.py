from datetime import datetime, timedelta

from django.http import HttpResponse, Http404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.patients.models import Patient
from .exports import patient_history_pdf, revenue_excel


class PatientHistoryPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        if not Patient.objects.filter(pk=patient_id).exists():
            raise Http404
        pdf = patient_history_pdf(patient_id)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="patient_{patient_id}_history.pdf"'
        return response


class RevenueExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        end = timezone.now().date()
        start = end - timedelta(days=int(request.query_params.get('days', 30)))

        if request.query_params.get('start'):
            start = datetime.strptime(request.query_params['start'], '%Y-%m-%d').date()
        if request.query_params.get('end'):
            end = datetime.strptime(request.query_params['end'], '%Y-%m-%d').date()

        excel_bytes = revenue_excel(start, end)
        response = HttpResponse(
            excel_bytes,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        filename = f'revenue_{start}_{end}.xlsx'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
