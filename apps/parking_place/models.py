import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.shared.models import DatedModel


def build_select_criteria():
    return {
        "regular": {
            "accessible_parking": False,
            "ev_parking": False,
        },
        "ev": {
            "accessible_parking": False,
            "ev_parking": True,
        },
        "accessible": {
            "accessible_parking": True,
            "ev_parking": False,
        },
    }


class Vehicle(DatedModel):
    """
    A vehicle; a car with a licence plate, optionally named.
    """

    name: str = models.CharField(max_length=255, null=True, blank=True)

    class Powertrains(models.TextChoices):
        ICE = "ICE"
        EV = "EV"

    license_plate: str = models.CharField(max_length=10)
    powertrain: str = models.CharField(
        max_length=64, choices=Powertrains.choices, default=Powertrains.ICE
    )


class ParkingPlace(DatedModel):
    """
    A place where cars park.
    """

    name: str = models.CharField(max_length=255, blank=True, null=True)

    address: str = models.CharField(max_length=255)
    postal_code: str = models.CharField(max_length=10)
    city: str = models.CharField(max_length=255)
    managed_by = models.ForeignKey(
        get_user_model(),
        related_name="managed_parking_space",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    @property
    def number_of_regular_parking_spaces(self):
        return self.parking_spaces.filter(**build_select_criteria()["regular"]).count()

    @property
    def number_of_ev_parking_spaces(self):
        return self.parking_spaces.filter(**build_select_criteria()["ev"]).count()

    @property
    def number_of_accessible_parking_spaces(self):
        return self.parking_spaces.filter(
            **build_select_criteria()["accessible"]
        ).count()

    @property
    def total_capacity(self):
        return self.parking_spaces.count()

    @property
    def available_regular_spaces(self):
        return self.parking_spaces.filter(
            state="AVAILABLE", **build_select_criteria()["regular"]
        ).count()

    @property
    def available_ev_spaces(self):
        return self.parking_spaces.filter(
            state="AVAILABLE", **build_select_criteria()["ev"]
        ).count()

    @property
    def available_accessible_spaces(self):
        return self.parking_spaces.filter(
            state="AVAILABLE", **build_select_criteria()["accessible"]
        ).count()


class ParkingSpaceQuerySet(models.QuerySet):
    def available_spaces_within(self, reserve_start, reserve_end, space_type=None):
        from apps.reservation.models import Reservation

        if reserve_start < datetime.datetime.now().replace(
            tzinfo=datetime.timezone.utc
        ):
            raise ValidationError("cannot reserve for past time.")

        all_available_spaces_by_type = (
            self.filter(**build_select_criteria()[space_type]) if space_type else self
        )
        reservations = Reservation.objects.filter(
            reservation_end__gte=reserve_start,
            reservation_start__lt=reserve_end,
            reservation_status__in=["RESERVED", "ONGOING"]
        ).values_list(
            'parking_space_id', flat=True)

        return all_available_spaces_by_type.exclude(

                id__in=reservations

        )


class ParkingSpace(DatedModel):
    """
    An allocated space in which to park your car.
    """

    class State(models.TextChoices):
        AVAILABLE = "AVAILABLE"
        OCCUPIED = "OCCUPIED"
        UNKNOWN = "UNKNOWN"

    name: str = models.CharField(max_length=255, null=True)
    price_per_minute: Decimal = models.DecimalField(
        default=0.0, max_digits=8, decimal_places=2
    )

    state: str = models.CharField(
        max_length=64, choices=State.choices, default=State.AVAILABLE
    )

    accessible_parking: bool = models.BooleanField(default=False)
    ev_parking: bool = models.BooleanField(default=False)

    parking_place = models.ForeignKey(
        "ParkingPlace", on_delete=models.CASCADE, related_name="parking_spaces"
    )
    objects = ParkingSpaceQuerySet.as_manager()

    @property
    def regular_parking(self):
        return bool(not (self.ev_parking or self.accessible_parking))
