"""
Vehicle factory module
"""

import factory
from factory import fuzzy

from apps.parking_place.models import Vehicle


class VehicleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vehicle

    name = factory.Faker("name")
    license_plate = factory.Faker("license_plate")
    powertrain = fuzzy.FuzzyChoice(["ICE", "EV"])
