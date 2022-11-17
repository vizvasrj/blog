
from django.dispatch import receiver

from django.db.models.signals import post_save
from users.models import User
from accounts.models import Profile
@receiver(post_save, sender=User)
def pre_save_receiver(sender, instance, created=False,  *args, **kwargs):
    if created:
        p = Profile.objects.create(user=instance)
        print(p.user)
