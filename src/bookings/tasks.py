from datetime import timedelta
from typing import Iterable

from anymail.message import AnymailMessage
from celery import shared_task
from celery.canvas import group
from django.conf import settings
from django.core import mail
from django.utils import timezone

from bookings import models


@shared_task(
    name="send_confirmation_email",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def send_confirmation_email(booking_id: str, template_id: str) -> None:
    """Send booking confirmation email."""
    booking: models.Booking = models.Booking.objects.get(id=booking_id)
    with mail.get_connection() as connection:
        message = AnymailMessage(
            subject="Booking confirmed",
            body=f"Your booking on the {booking.room.hotel} has been confirmed.",
            to=[booking.client.email],
            connection=connection,
        )
        message.template_id = template_id
        message.send(False)
    booking.confirm()


@shared_task(name="cancel_unchecked_bookings")
def cancel_unchecked_bookings():
    """Cancel bookings where the client did not check in."""
    one_day_ago = timezone.now() - timedelta(days=1)
    unchecked_bookings: Iterable[models.Booking] = models.Booking.objects.unchecked(
        one_day_ago
    )
    for booking in unchecked_bookings:
        booking.cancel()


@shared_task(name="retry_send_confirmation_email_for_pending_bookings")
def retry_send_confirmation_email_for_pending_bookings():
    """Retry sending confirmation email for pending bookings."""
    pending_bookings: Iterable[models.Booking] = models.Booking.objects.pending()
    send_confirmation_tasks = group(
        send_confirmation_email.s(
            booking.id, settings.BOOKINGS_CONFIRMATION_EMAIL_TEMPLATE_ID
        )
        for booking in pending_bookings
    )
    send_confirmation_tasks.apply_async()
