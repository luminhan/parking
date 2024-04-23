"""
Parking Place Factory module
"""

import factory

from apps.parking_place.models import ParkingPlace


class ParkingPlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ParkingPlace

    name = factory.Faker("name")
    city = factory.Faker("city")
    postal_code = factory.Faker("postalcode")
    address = factory.Faker("address")
