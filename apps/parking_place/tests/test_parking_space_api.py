"""
Test for the parking space API
"""

from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from apps.parking_place.models import ParkingSpace
from apps.parking_place.serializers import ParkingSpaceSerializer
from apps.parking_place.tests.factory.parking_place_factory import ParkingPlaceFactory

from apps.parking_place.tests.factory.parking_space_factory import ParkingSpaceFactory
from apps.shared.tests.factory.user import UserFactory


class PublicParkingPlaceAPITest(TestCase):
    """
    Test the publicly available parking space API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(reverse("parking-space-list"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateParkingPlaceAPITestList(TestCase):
    """
    Test the authorized user parking space API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.parking_place = ParkingPlaceFactory(managed_by=self.user)
        self.parking_space = ParkingSpaceFactory.create_batch(
            5, parking_place=self.parking_place
        )

    def test_list_parking_places(self):
        res = self.client.get(reverse("parking-space-list"))
        parking_spaces = ParkingSpace.objects.all()
        serializer = ParkingSpaceSerializer(parking_spaces, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)


class PrivateParkingPlaceAPITestDetail(TestCase):
    """
    Test the authorized user parking space API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.parking_place = ParkingPlaceFactory(managed_by=self.user)
        self.parking_space = ParkingSpaceFactory(parking_place=self.parking_place)

    def test_detail_parking_space(self):
        res = self.client.get(
            reverse("parking-space-detail", args=[self.parking_space.id])
        )
        parking_space = ParkingSpace.objects.get(id=self.parking_space.id)
        serializer = ParkingSpaceSerializer(parking_space)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_parking_space_disable(self):
        res = self.client.post(
            reverse("parking-space-list"),
            {"parking_place": self.parking_place.id, "name": "test", "status": "A"},
        )
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_parking_space_disable(self):
        res = self.client.put(
            reverse("parking-space-detail", args=[self.parking_space.id]),
            {"parking_place": self.parking_place.id, "name": "test", "status": "A"},
        )
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_parking_space_disable(self):
        res = self.client.delete(
            reverse("parking-space-detail", args=[self.parking_space.id])
        )
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
