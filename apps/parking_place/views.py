import datetime

from rest_framework import viewsets

from apps.parking_place.filters import ParkingSpaceFilterSet
from apps.parking_place.models import ParkingPlace, ParkingSpace, Vehicle
from apps.parking_place.serializers import (
    ParkingPlaceSerializer,
    ParkingSpaceSerializer,
    ParkingSpaceAvailableWithinTimeRangeSerializer, VehicleSerializer,
)

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    filterset_fields = ["name", "license_plate", "powertrain"]


class ParkingPlaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParkingPlaceSerializer
    filterset_fields = ["city", "postal_code"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ParkingPlace.objects.all()
        return ParkingPlace.objects.filter(managed_by=self.request.user)


class AvailableParkingSpacesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParkingSpaceAvailableWithinTimeRangeSerializer

    def get_queryset(self):
        date_format = "%Y-%m-%dT%H:%M:%S.%f%z"

        reserve_start = self.request.query_params.get("reserve_start")
        if not reserve_start:
            raise ValueError("reserve_start is required")
        reserve_start = datetime.datetime.strptime(reserve_start, date_format).replace(
            tzinfo=datetime.timezone.utc
        )
        reserve_end = self.request.query_params.get("reserve_end")
        if not reserve_end:
            raise ValueError("reserve_end is required")
        reserve_end = datetime.datetime.strptime(reserve_end, date_format).replace(
            tzinfo=datetime.timezone.utc
        )
        space_type = self.request.query_params.get("space_type")
        if self.request.user.is_superuser:
            return ParkingSpace.objects.available_spaces_within(
                reserve_start, reserve_end, space_type
            )
        return ParkingSpace.objects.available_spaces_within(
            reserve_start, reserve_end, space_type
        ).filter(parking_place__managed_by=self.request.user)


class ParkingSpaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParkingSpaceSerializer
    filterset_class = ParkingSpaceFilterSet

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ParkingSpace.objects.all()
        return ParkingSpace.objects.filter(parking_place__managed_by=self.request.user)
