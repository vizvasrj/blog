from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify
from unidecode import unidecode
from .models import Post, Category


@receiver(pre_save, sender=Post)
def pre_save_receiver(sender, instance, created=False,  *args, **kwargs):
    if instance._state.adding:
        try:
            last_id = Post.objects.latest('id').id + 1
        except Post.DoesNotExist:
            last_id = 1
        instance.slug = f'{slugify(unidecode(instance.title))}-{hex(last_id)}'


@receiver(pre_save, sender=Category)
def pre_save_receiver(sender, instance, created=False,  *args, **kwargs):
    if instance._state.adding:
        try:
            last_id = Category.objects.latest('id').id + 1
        except Category.DoesNotExist:
            last_id = 1
        instance.slug = f'{slugify(unidecode(instance.name))}-{hex(last_id)}'
