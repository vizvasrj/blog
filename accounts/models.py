from django.db import models
from django.urls import reverse

from users.models import User
from django.utils.translation import gettext as _
# Create your models here.
class Profile(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profiles',
        verbose_name=_("user")
    )   
    # point = models.ManyToManyField(
    #     Points,
    #     related_name='profile_point'
    #     )
    photo = models.ImageField(
        _("photo"),
        upload_to='users/%Y/%m/%d',
        blank=True,
        null=True,
        default='users/default.webp'
    )
    about = models.CharField(
        _("about"),
        max_length=150,
        blank=True,
        null=True
    )
    # register_language = models.ManyToManyField(MyLanguages, related_name='registerd_lns')
    timezone = models.IntegerField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    # This will use to get suggestion from users Post 
    # or random other similar post. 
    # (simalar_post || mypost)
    similar_post = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user_detail' ,kwargs={"username":self.user.username})

    def get_user_url(self):
        return reverse('user_detail' ,kwargs={"username":self.user.username})


