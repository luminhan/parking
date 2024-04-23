from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.reservation.views import ReservationViewSet

router = DefaultRouter()

router.register(r"reservation", ReservationViewSet, basename="reservation")

urlpatterns = [
    path("", include(router.urls)),
]
