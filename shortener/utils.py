import datetime

from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string


def get_future_date_from_today(days):
    return timezone.now().date() + datetime.timedelta(days=days)


def get_date_one_week_from_today():
    return get_future_date_from_today(days=7)


def get_date_three_months_from_today():
    return get_future_date_from_today(days=90)


def get_date_one_year_from_today():
    return get_future_date_from_today(days=365)


def get_random_generated_shortcode(k=settings.URLTAG_LENGTH):
    return get_random_string(k)
