from django.db.models.signals import post_delete,post_save,pre_save,post_init
from django.dispatch import receiver
from .models import Meeting
from datetime import date

@receiver(pre_save, sender=Meeting)
def delete_profile_photo(sender, instance:Meeting, **kwargs):
    to_delete=Meeting.objects.all().exclude(created_at__date=date.today())
    if to_delete:
            to_delete.delete()
            ...