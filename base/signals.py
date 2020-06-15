from django.db.models.signals import post_save
from django.dispatch import receiver

from base.models import Transaction


@receiver(post_save, sender=Transaction)
def update_balance(sender, instance, **kwargs):
    instance.sender.update_balance()
    instance.recipient.update_balance()
