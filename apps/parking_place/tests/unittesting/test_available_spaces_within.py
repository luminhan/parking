"""
Test the available spaces within a parking place
"""

from django.test import TestCase
from pytz import UTC

from apps.parking_place.models import ParkingSpace
from apps.parking_place.tests.factory.parking_place_factory import ParkingPlaceFactory
from apps.parking_place.tests.factory.parking_space_factory import ParkingSpaceFactory
from apps.parking_place.tests.factory.vehicle_factory import VehicleFactory
from apps.reservation.tests.factory.reservation_factory import ReservationFactory
from apps.shared.tests.factory.user import UserFactory
from datetime import datetime
from freezegun import freeze_time


class TestAvailableSpacesTestCase(TestCase):
    def setUp(self):

        self.user = UserFactory()
        self.vehicle = VehicleFactory()
        self.parking_place = ParkingPlaceFactory(managed_by=self.user)
        self.parking_space_1 = ParkingSpaceFactory(parking_place=self.parking_place)
        self.parking_space_2 = ParkingSpaceFactory(parking_place=self.parking_place)
        self.reservation = ReservationFactory(
            parking_space=self.parking_space_1,
            parking_place=self.parking_place,
            vehicle=self.vehicle,
            reservation_start=datetime(2024, 1, 1, 13, 00, tzinfo=UTC),
            reservation_end=datetime(2024, 1, 1, 14, 00, tzinfo=UTC),
        )

    @freeze_time("2024-01-01")
    def test_all_spaces_available(self):

        parking_spaces = ParkingSpace.objects.available_spaces_within(
            datetime(2024, 1, 1, 15, 00, tzinfo=UTC),
            datetime(2024, 1, 1, 16, 00, tzinfo=UTC),
        )
        self.assertEqual(len(parking_spaces), 2)

    @freeze_time("2024-01-01")
    def test_one_space_available(self):

        parking_spaces = ParkingSpace.objects.available_spaces_within(
            datetime(2024, 1, 1, 13, 30, tzinfo=UTC),
            datetime(2024, 1, 1, 14, 30, tzinfo=UTC),
        )
        self.assertEqual(len(parking_spaces), 1)
        # Check if the available space is the one that is not reserved
        self.assertEqual(parking_spaces[0], self.parking_space_2)

    @freeze_time("2024-01-01")
    def test_no_space_available(self):
        # make another reservation on the second parking space
        ReservationFactory(
            parking_space=self.parking_space_2,
            parking_place=self.parking_place,
            vehicle=self.vehicle,
            reservation_start=datetime(2024, 1, 1, 13, 30, tzinfo=UTC),
            reservation_end=datetime(2024, 1, 1, 14, 30, tzinfo=UTC),
        )
        parking_spaces = ParkingSpace.objects.available_spaces_within(
            datetime(2024, 1, 1, 13, 30, tzinfo=UTC),
            datetime(2024, 1, 1, 14, 30, tzinfo=UTC),
        )
        self.assertEqual(len(parking_spaces), 0)
