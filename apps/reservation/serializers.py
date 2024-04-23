from rest_framework import serializers

from apps.parking_place.models import Vehicle, ParkingPlace, ParkingSpace
from apps.reservation.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    vehicle_license_plate = serializers.CharField(
        source="vehicle.license_plate", read_only=True
    )
    parking_place_name = serializers.CharField(
        source="parking_place.name", read_only=True
    )
    parking_space_name = serializers.CharField(
        source="parking_space.name", read_only=True
    )
    # write only fields
    vehicle = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(), write_only=True
    )
    parking_place = serializers.PrimaryKeyRelatedField(
        queryset=ParkingPlace.objects.all(), write_only=True
    )
    parking_space = serializers.PrimaryKeyRelatedField(
        queryset=ParkingSpace.objects.all(), write_only=True
    )

    class Meta:
        model = Reservation
        fields = [
            "id",
            "reservation_start",
            "reservation_end",
            "parking_start",
            "parking_end",
            "reservation_status",
            "amount",
            "actual_amount",
            "surcharge_amount",
            "vehicle_license_plate",
            "parking_place_name",
            "parking_space_name",
            "vehicle",
            "parking_place",
            "parking_space",
        ]
