from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import register, login, logout, DoctorListViewSet, DoctorViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorListViewSet)
router.register(r'doctor-details', DoctorViewSet)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', include(router.urls)),
]
