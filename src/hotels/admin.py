from django.contrib import admin

from hotels import models


@admin.register(models.Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "phone_number", "owner", "manager"]
    search_fields = [
        "name",
        "address__city",
        "address__uf",
        "phone_number",
        "email",
        "owner__email",
        "manager__email",
    ]
    list_filter = ["address"]


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["hotel", "number", "floor", "room_type"]
    search_fields = ["hotel__name", "number", "floor"]
    list_filter = ["room_type"]
