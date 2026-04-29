"""Polyclinic Project URL configuration."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


api_v1 = [
    path('patients/',  include('apps.patients.urls')),
    path('doctors/',   include('apps.doctors.urls')),
    path('visits/',    include('apps.visits.urls')),
    path('billing/',   include('apps.billing.urls')),
    path('reports/',   include('apps.reports.urls')),

    # Auth
    path('auth/login/',   TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(),    name='token_refresh'),
    path('auth/verify/',  TokenVerifyView.as_view(),     name='token_verify'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',   include(api_v1)),

    # API documentation
    path('api/schema/',          SpectacularAPIView.as_view(),       name='schema'),
    path('api/docs/',            SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/',           SpectacularRedocView.as_view(url_name='schema'),   name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# --- Admin site customization ---
admin.site.site_header = "Poliklinika Boshqaruv Tizimi"
admin.site.site_title  = "Poliklinika Admin"
admin.site.index_title = "Boshqaruv paneli"
