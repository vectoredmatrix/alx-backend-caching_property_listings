# properties/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

@receiver([post_save, post_delete], sender=Property)
def clear_all_properties_cache(sender, **kwargs):
    print("Invalidating 'all_properties' cache...")
    cache.delete('all_properties')
