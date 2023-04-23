from django.dispatch import receiver
from django.db.models.signals import post_save

from config import settings
from store.models import Profile


@receiver(signal=post_save, sender=settings.AUTH_USER_MODEL)
def make_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])