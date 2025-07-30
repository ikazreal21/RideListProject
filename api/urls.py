from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'rides', views.RideViewSet, basename='ride')
router.register(r'ride-events', views.RideEventViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]