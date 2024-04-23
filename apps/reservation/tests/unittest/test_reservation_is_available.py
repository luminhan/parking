"""
Test the intended reservation is available
"""

from datetime import datetime

from django.test import TestCase
from pytz import UTC

from apps.parking_place.tests.factory.parking_place_factory import ParkingPlaceFactory
from apps.parking_place.tests.factory.parking_space_factory import ParkingSpaceFactory
from apps.parking_place.tests.factory.vehicle_factory import VehicleFactory
from apps.reservation.models import Reservation
from apps.reservation.tests.factory.reservation_factory import ReservationFactory
from apps.shared.tests.factory.user import UserFactory


class TestReservationIsAvailable(TestCase):
    def setUp(self):

        self.user = UserFactory()
        self.vehicle = VehicleFactory()
        self.parking_place = ParkingPlaceFactory(managed_by=self.user)
        self.parking_space_1 = ParkingSpaceFactory(parking_place=self.parking_place)

        self.reservation = ReservationFactory(
            parking_space=self.parking_space_1,
            parking_place=self.parking_place,
            vehicle=self.vehicle,
            reservation_start=datetime(2024, 1, 1, 13, 00, tzinfo=UTC),
            reservation_end=datetime(2024, 1, 1, 14, 00, tzinfo=UTC),
        )

    def test_reservation_is_available(self):

        is_available = Reservation.objects.is_available(
            datetime(2024, 1, 1, 15, 00, tzinfo=UTC),
            datetime(2024, 1, 1, 16, 00, tzinfo=UTC),
        )
        self.assertTrue(is_available)

    def test_reservation_is_not_available(self):
        is_available = Reservation.objects.is_available(
            datetime(2024, 1, 1, 13, 30, tzinfo=UTC),
            datetime(2024, 1, 1, 14, 30, tzinfo=UTC),
        )
        self.assertFalse(is_available)
