"""
Test for the parking place API
"""

from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from apps.parking_place.models import ParkingPlace
from apps.parking_place.serializers import ParkingPlaceSerializer
from apps.parking_place.tests.factory.parking_place_factory import ParkingPlaceFactory
from apps.shared.tests.factory.user import UserFactory


class PublicParkingPlaceAPITest(TestCase):
    """
    Test the publicly available parking place API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(reverse('parking-place-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateParkingPlaceAPITestList(TestCase):
    """
    Test the authorized user parking place API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.parking_place = ParkingPlaceFactory(managed_by=self.user)


    def test_list_parking_places(self):
        res = self.client.get(reverse('parking-place-list'))
        parking_places = ParkingPlace.objects.all()
        serializer = ParkingPlaceSerializer(parking_places, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

class PrivateParkingPlaceAPITestDetail(TestCase):
    """
    Test the authorized user parking place API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.parking_place = ParkingPlaceFactory(managed_by=self.user)

    def test_detail_parking_place(self):
        res = self.client.get(reverse('parking-place-detail', args=[self.parking_place.id]))
        parking_place = ParkingPlace.objects.get(id=self.parking_place.id)
        serializer = ParkingPlaceSerializer(parking_place)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_parking_place_disable(self):
        payload = {
            'name': 'Test Parking Place',
            'city': 'Test City',
            'postal_code': '12345',
            'address': 'Test Address',
            'managed_by': self.user.id
        }
        res = self.client.post(reverse('parking-place-list'), payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_parking_place_disable(self):
        payload = {
            'name': 'Test Parking Place',
            'city': 'Test City',
            'postal_code': '12345',
            'address': 'Test Address',
            'managed_by': self.user.id
        }
        res = self.client.put(reverse('parking-place-detail', args=[self.parking_place.id]), payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_parking_place_disable(self):
        res = self.client.delete(reverse('parking-place-detail', args=[self.parking_place.id]))
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_filter_parking_places(self):
        res = self.client.get(reverse('parking-place-list'),
                              {'city': self.parking_place.city})
        parking_places = ParkingPlace.objects.filter(city=self.parking_place.city)
        serializer = ParkingPlaceSerializer(parking_places, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)


