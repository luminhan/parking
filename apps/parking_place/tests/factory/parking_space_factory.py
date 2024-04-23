"""
Parking Space Factory module
"""

import factory
from factory import fuzzy

from apps.parking_place.models import ParkingSpace


class ParkingSpaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ParkingSpace

    name = factory.Faker("name")
    state = fuzzy.FuzzyChoice(["AVAILABLE", "OCCUPIED"])
    accessible_parking = fuzzy.FuzzyChoice([True, False])
    ev_parking = fuzzy.FuzzyChoice([True, False])
    price_per_minute = fuzzy.FuzzyDecimal(0.30, 0.60)
