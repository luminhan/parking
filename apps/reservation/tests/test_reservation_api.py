"""
Test for reservation API
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from apps.reservation.models import Reservation
from apps.reservation.serializers import ReservationSerializer
from apps.reservation.tests.factory.reservation_factory import ReservationFactory

from apps.parking_place.tests.factory.parking_place_factory import ParkingPlaceFactory
from apps.parking_place.tests.factory.parking_space_factory import ParkingSpaceFactory
from apps.parking_place.tests.factory.vehicle_factory import VehicleFactory
from apps.shared.tests.factory.user import UserFactory


class PublicReservationAPITest(TestCase):
    """
    Test the publicly available reservation API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(reverse("reservation-list"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReservationAPITestList(TestCase):
    """
    Test the authorized user reservation API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.parking_place = ParkingPlaceFactory(managed_by=self.user)
        self.parking_space = ParkingSpaceFactory(parking_place=self.parking_place)
        self.vehicle = VehicleFactory()
        self.reservation = ReservationFactory(
            parking_space=self.parking_space,
            parking_place=self.parking_place,
            vehicle=self.vehicle,
        )

    def test_list_reservations(self):
        res = self.client.get(reverse("reservation-list"))
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)


class PrivateReservationAPITestDetail(TestCase):
    """
    Test the authorized user reservation API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.parking_place = ParkingPlaceFactory(managed_by=self.user)
        self.parking_space = ParkingSpaceFactory(parking_place=self.parking_place)
        self.vehicle = VehicleFactory()
        self.reservation = ReservationFactory(
            parking_space=self.parking_space,
            parking_place=self.parking_place,
            vehicle=self.vehicle,
        )

    def test_retrieve_reservation(self):
        res = self.client.get(reverse("reservation-detail", args=[self.reservation.id]))
        serializer = ReservationSerializer(self.reservation)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_reservation(self):
        payload = {
            "reservation_status": "CANCELLED",
        }
        res = self.client.patch(
            reverse("reservation-detail", args=[self.reservation.id]), payload
        )
        self.reservation.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.reservation.reservation_status, payload["reservation_status"]
        )

    def test_delete_reservation(self):
        res = self.client.delete(
            reverse("reservation-detail", args=[self.reservation.id])
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 0)
