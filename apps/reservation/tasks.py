from apps.parking_place.models import ParkingSpace
from project import celery_app as app
from apps.reservation.models import Reservation
from django.utils import timezone


@app.task
def release_expired_reservations():

    reservations = Reservation.objects.filter(
        reservation_end__lt=timezone.now(),
        reservation_status=Reservation.ReservationStatuses.RESERVED,
    )
    reservations_list = reservations.values_list("id", flat=True)
    if reservations:
        ParkingSpace.objects.filter(reservations__in=reservations_list).update(
            state=ParkingSpace.State.AVAILABLE
        )
        reservations.delete()

    cancelled_reservations = Reservation.objects.filter(
        reservation_status=Reservation.ReservationStatuses.CANCELLED
    )
    cancelled_reservations.delete()
