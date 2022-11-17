# import imp
# from django.dispatch import receiver

# from django.db.models.signals import post_save, post_delete
# from .models import Contact
# # from actions.models import Notification

# from django.utils.translation import gettext_lazy as _
# from django.urls import reverse

# @receiver(post_save, sender=Contact)
# def send_notification_to(sender, created, instance, *args, **kwargs):
#     if created:
#         # Notification.objects.create(
#         #     message=_('%(user_from)s followed you.') % {'user_from': instance.user_from},
#         #     user=instance.user_to,
#         #     link=reverse('user_follower', kwargs={"username": instance.user_to.username})
#         # )
#         Notification.objects.create(
#             types=1,
#             user_from=instance.user_from,
#             user=instance.user_to,
#             message=_('%(user_from)s followed you.') % {'user_from': instance.user_from},
#         )
#         print('FOLLOWWED')


# @receiver(post_delete, sender=Contact)
# def send_notification_on_unfollow(sender, instance, *args, **kwargs):
#     # Notification.objects.create(
#     #     message=_('%(user_from)s unfollowed you.') % {'user_from': instance.user_from},
#     #     user=instance.user_to,
#     #     link=reverse('user_follower', kwargs={"username": instance.user_to.username})
#     # )
#     Notification.objects.create(
#             types=2,
#             user_from=instance.user_from,
#             user=instance.user_to,
#             message=_('%(user_from)s unfollowed you.') % {'user_from': instance.user_from},
#         )
#     print('UNFOLLOWED')
