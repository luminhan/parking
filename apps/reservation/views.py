from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from apps.reservation.models import Reservation
from apps.reservation.serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start = serializer.validated_data["reservation_start"]
        end = serializer.validated_data["reservation_end"]
        if self.get_queryset().is_available(start, end):
            return super().create(request, *args, **kwargs)
        raise ValidationError("Parking place is not available at that time "
                              "slot. Please choose another time slot.")

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Reservation.objects.all()
        return Reservation.objects.filter(parking_place__managed_by=self.request.user)
