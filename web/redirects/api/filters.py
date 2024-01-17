from django_filters import rest_framework as filters, BaseInFilter, NumberFilter

from redirects.models import PhysicalTag


class NumberInFilter(BaseInFilter, NumberFilter):
    pass

class PhysicalTagFilter(filters.FilterSet):
    class Meta:
        model = PhysicalTag
        fields = ["active", "tag_type", "id"]

    id__in = NumberInFilter(field_name="id")

