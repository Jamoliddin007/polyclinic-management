from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DiscountCategoryViewSet

router = DefaultRouter()
router.register('patients', PatientViewSet, basename='patient')
router.register('discount-categories', DiscountCategoryViewSet, basename='discount-category')

urlpatterns = router.urls
