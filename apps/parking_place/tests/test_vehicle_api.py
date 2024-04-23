"""
Test for vehicle api
"""
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from apps.parking_place.models import Vehicle
from apps.parking_place.serializers import VehicleSerializer
from apps.parking_place.tests.factory.vehicle_factory import VehicleFactory
from apps.shared.tests.factory.user import UserFactory


class PublicVehicleAPITest(TestCase):
    """
    Test the publicly available vehicle API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(reverse('vehicle-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateVehicleAPITestList(TestCase):
    """
    Test the authorized user vehicle API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.vehicle = VehicleFactory.create_batch(5)

    def test_list_vehicles(self):
        res = self.client.get(reverse('vehicle-list'))
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

class PrivateVehicleAPITestDetail(TestCase):
    """
    Test the authorized user vehicle API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.vehicle = VehicleFactory.create_batch(5)


    def test_detail_vehicle(self):
        res = self.client.get(reverse('vehicle-detail', args=[self.vehicle[0]
                                      .id]))
        vehicle = Vehicle.objects.get(id=self.vehicle[0].id)
        serializer = VehicleSerializer(vehicle)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_vehicle(self):
        payload = {
            'license_plate': '1234',
            'name': 'test car',
            'powertrain': 'ICE'
        }
        res = self.client.post(reverse('vehicle-list'), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_vehicle(self):
        payload = {
            'license_plate': '1234',
            'name': 'test car',
            'powertrain': 'EV'
        }
        res = self.client.put(reverse('vehicle-detail', args=[self.vehicle[0]
                                      .id]), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['powertrain'], 'EV')

    def test_filter_vehicle(self):
        res = self.client.get(reverse('vehicle-list'), {'license_plate':
                                                            self.vehicle[
                                                                0].license_plate})
        vehicles = Vehicle.objects.filter(license_plate=self.vehicle[0]
                                          .license_plate)
        serializer = VehicleSerializer(vehicles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_delete_vehicle(self):
        res = self.client.delete(reverse('vehicle-detail', args=[
            self.vehicle[0].id]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vehicle.objects.filter(id=self.vehicle[0].id).count(), 0)



