from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from bookings import models, tasks


@receiver(post_save, sender=models.Booking, dispatch_uid="send_confirmation_on_create")
def send_confirmation_on_create(
    sender: type[models.Booking], instance: models.Booking, created: True, **kwargs
):
    """Send confirmation email when a booking is created."""
    if created:
        tasks.send_confirmation_email.delay(
            instance.id, settings.BOOKINGS_CONFIRMATION_EMAIL_TEMPLATE_ID
        )
