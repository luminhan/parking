from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.parking_place.views import (
    ParkingPlaceViewSet,
    ParkingSpaceViewSet,
    AvailableParkingSpacesViewSet, VehicleViewSet,
)

router = DefaultRouter()

router.register(r"parking-place", ParkingPlaceViewSet, basename="parking-place")
router.register(r"parking-space", ParkingSpaceViewSet, basename="parking-space")
router.register(
    r"available-parking-spaces",
    AvailableParkingSpacesViewSet,
    basename="available-parking-spaces",
)
router.register(r"vehicle", VehicleViewSet, basename="vehicle")

urlpatterns = [
    path("", include(router.urls)),
]
