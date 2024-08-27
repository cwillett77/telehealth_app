from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailabilityViewSet

router = DefaultRouter()
router.register(r'availabilities', AvailabilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('availabilities/<int:doctor_id>/<int:pk>/', AvailabilityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='availability-detail'),
]
