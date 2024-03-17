from django_filters.rest_framework import CharFilter, FilterSet

from addresses.models import Address


class AddressFilter(FilterSet):
    city = CharFilter(field_name="city", lookup_expr="icontains")
    street = CharFilter(field_name="street", lookup_expr="icontains")
    uf = CharFilter(field_name="uf", lookup_expr="iexact")
    zip_code = CharFilter(field_name="zip_code", lookup_expr="iexact")

    class Meta:
        model = Address
        fields = ["city", "uf", "zip_code", "street"]
