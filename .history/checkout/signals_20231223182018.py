from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem

@receiver(post_save)
def update_on_save(sender, instance, created, **kwargs):

    instance.order.update_total()
