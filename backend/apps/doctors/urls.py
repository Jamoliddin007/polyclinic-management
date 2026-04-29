from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, SpecialtyViewSet, QualificationViewSet

router = DefaultRouter()
router.register('doctors', DoctorViewSet, basename='doctor')
router.register('specialties', SpecialtyViewSet, basename='specialty')
router.register('qualifications', QualificationViewSet, basename='qualification')

urlpatterns = router.urls
