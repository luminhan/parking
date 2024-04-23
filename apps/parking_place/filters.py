from django_filters import CharFilter, BooleanFilter
from django_filters.rest_framework import FilterSet

from apps.parking_place.models import ParkingSpace, build_select_criteria


class ParkingSpaceFilterSet(FilterSet):
    parking_place = CharFilter(
        field_name="parking_place__name", lookup_expr="icontains"
    )
    city = CharFilter(field_name="parking_place__city", lookup_expr="icontains")
    ev = BooleanFilter(method="filter_parking")
    accessible = BooleanFilter(method="filter_parking")
    regular = BooleanFilter(method="filter_parking")

    class Meta:
        model = ParkingSpace
        fields = ["parking_place", "city", "ev", "accessible", "regular"]

    def filter_parking(self, queryset, name, value):
        return queryset.filter(**build_select_criteria()[name])
