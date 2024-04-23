from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.parking_place.models import Vehicle, ParkingPlace, ParkingSpace
from apps.shared.models import DatedModel


class ReservationQuerySet(models.QuerySet):
    def is_available(self, start, end):
        return not self.filter(
            reservation_end__gte=start,
            reservation_start__lt=end,
            reservation_status__in=[
                Reservation.ReservationStatuses.RESERVED,
                Reservation.ReservationStatuses.ONGOING,
            ],
        ).exists()


class Reservation(DatedModel):
    """
    A reservation for a parking space
    """

    class ReservationStatuses(models.TextChoices):
        RESERVED = "RESERVED"
        CANCELLED = "CANCELLED"
        COMPLETED = "COMPLETED"
        ONGOING = "ONGOING"

    reservation_start = models.DateTimeField(db_index=True)
    reservation_end = models.DateTimeField(db_index=True)
    parking_start = models.DateTimeField(db_index=True, null=True)
    parking_end = models.DateTimeField(db_index=True, null=True)
    reservation_status = models.CharField(
        max_length=16,
        choices=ReservationStatuses.choices,
        default=ReservationStatuses.RESERVED,
    )
    amount: Decimal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    surcharge_amount: Decimal = models.DecimalField(
        default=0.0, max_digits=8, decimal_places=2
    )
    actual_amount: Decimal = models.DecimalField(
        default=0.0, max_digits=8, decimal_places=2
    )

    vehicle: Vehicle = models.ForeignKey(
        Vehicle, related_name="reservations", on_delete=models.CASCADE
    )
    parking_place: ParkingPlace = models.ForeignKey(
        ParkingPlace, related_name="reservations", on_delete=models.CASCADE
    )

    parking_space: ParkingSpace = models.ForeignKey(
        ParkingSpace, related_name="reservations", on_delete=models.CASCADE
    )
    objects = ReservationQuerySet.as_manager()


@receiver(pre_save, sender=Reservation)
def calculate_amount_to_charge(sender, instance, **kwargs):

    if instance._state.adding:
        # Calculate amount to charge
        time_difference = instance.reservation_end - instance.reservation_start
        amount = (
            Decimal(time_difference.total_seconds() / 60)
            * instance.parking_space.price_per_minute
        )
        instance.amount = amount

    else:
        if instance.parking_end:
            # Calculate actual amount to charge
            time_difference = instance.parking_end - instance.reservation_start
            actual_amount = (
                Decimal(time_difference.total_seconds() / 60)
                * instance.parking_space.price_per_minute
            )
            instance.actual_amount = actual_amount
            instance.surcharge_amount = actual_amount - instance.amount
            instance.reservation_status = Reservation.ReservationStatuses.COMPLETED
            instance.parking_place.state = "AVAILABLE"
        elif instance.parking_start:
            instance.reservation_status = Reservation.ReservationStatuses.ONGOING
        elif instance.reservation_status == Reservation.ReservationStatuses.CANCELLED:
            instance.parking_place.state = "AVAILABLE"
