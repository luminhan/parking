from rest_framework import serializers

from apps.parking_place.models import ParkingPlace, ParkingSpace, Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["id", "name", "license_plate", "powertrain"]

class ParkingPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingPlace
        fields = [
            "id",
            "name",
            "city",
            "postal_code",
            "address",
            "total_capacity",
            "number_of_regular_parking_spaces",
            "number_of_ev_parking_spaces",
            "number_of_accessible_parking_spaces",
            "available_regular_spaces",
            "available_ev_spaces",
            "available_accessible_spaces",
        ]


class ParkingSpaceAvailableWithinTimeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpace
        fields = [
            "id",
            "name",
            "price_per_minute",
            "state",
            "ev_parking",
            "accessible_parking",
            "regular_parking",
        ]


class ParkingSpaceSerializer(serializers.ModelSerializer):
    parking_place = serializers.CharField(source="parking_place.name")

    class Meta:
        model = ParkingSpace
        fields = [
            "id",
            "name",
            "parking_place",
            "price_per_minute",
            "state",
            "ev_parking",
            "accessible_parking",
            "regular_parking",
        ]
