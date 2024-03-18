from django.contrib import admin

from bookings import models


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["room", "start", "end", "status", "client"]
    search_fields = ["room__hotel__name", "client__email"]
    list_filter = ["status"]

    @admin.action(description="Confirm selected bookings")
    def confirm_bookings(self, request, queryset):
        for booking in queryset:
            booking.confirm()
        self.message_user(request, "The selected bookings have been confirmed.")

    @admin.action(description="Cancel selected bookings")
    def cancel_bookings(self, request, queryset):
        for booking in queryset:
            booking.cancel()
        self.message_user(request, "The selected bookings have been canceled.")
