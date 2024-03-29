from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class UrlRecord(models.Model):
    short_url = models.CharField(
        primary_key=True,
        editable=False,
        max_length=settings.URLTAG_LENGTH
    )
    original_url = models.URLField(blank=False, null=False)
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    date_created = models.DateField(blank=True, auto_now_add=True)
    date_expiry = models.DateField()

    def __str__(self):
        return self.original_url

    @property
    def is_expired(self):
        return self.date_expiry < timezone.now().date()

    @classmethod
    def get_expired_anon_urlrecords(cls):
        return cls.objects.filter(user=None).filter(
            date_expiry__lt=timezone.now().date()
        )

    @classmethod
    def delete_expired_anon_urlrecords(cls):
        qs = cls.get_expired_anon_urlrecords()
        qs.delete()
        return None
