import os
from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import Profile

@receiver(post_delete, sender=Profile)
def delete_profile_photo(sender, instance:Profile, **kwargs):
    if instance.Photo_link:
        if os.path.isfile(instance.Photo_link.path):
            os.remove(instance.Photo_link.path)

@receiver(post_save, sender=Profile)
def create_emp_profile(sender, instance: Profile, created, **kwargs):
    if created and instance.Role.role_name=="MD":
        instance.Employee_id.is_superuser=True
        instance.Employee_id.save()
