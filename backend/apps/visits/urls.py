from rest_framework.routers import DefaultRouter
from .views import (
    VisitViewSet, ProcedureTypeViewSet,
    VisitProcedureViewSet, VisitConsultationViewSet,
)

router = DefaultRouter()
router.register('visits', VisitViewSet, basename='visit')
router.register('procedure-types', ProcedureTypeViewSet, basename='procedure-type')
router.register('visit-procedures', VisitProcedureViewSet, basename='visit-procedure')
router.register('visit-consultations', VisitConsultationViewSet, basename='visit-consultation')

urlpatterns = router.urls
