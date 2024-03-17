from django.contrib import admin

from addresses.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin for Address."""

    list_display = ("street", "city", "uf", "zip_code")
    search_fields = ("street", "city", "uf", "zip_code")
