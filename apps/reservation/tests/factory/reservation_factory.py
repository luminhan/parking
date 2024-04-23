"""
Reservation Factory module
"""

import factory
from factory.fuzzy import FuzzyDateTime
from datetime import datetime

from pytz import UTC

from apps.parking_place.tests.factory.parking_place_factory import ParkingPlaceFactory
from apps.parking_place.tests.factory.parking_space_factory import ParkingSpaceFactory
from apps.parking_place.tests.factory.vehicle_factory import VehicleFactory
from apps.reservation.models import Reservation


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation

    reservation_start = FuzzyDateTime(
        datetime(2022, 1, 1, tzinfo=UTC),
        datetime(2023, 1, 1, tzinfo=UTC),
    )
    reservation_end = FuzzyDateTime(
        datetime(2022, 1, 1, tzinfo=UTC),
        datetime(2023, 1, 1, tzinfo=UTC),
    )

    parking_space = factory.SubFactory(ParkingSpaceFactory)
    parking_place = factory.SubFactory(ParkingPlaceFactory)
    vehicle = factory.SubFactory(VehicleFactory)
