from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator

from .managers import CustomeUserManager

from .model_fields import LowercaseEMailField, LowercaseUsernameField




class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()


    # uid = models.UUIDField(
    #     unique=True, editable=False, default=uuid.uuid4,
    #     verbose_name=_('Public identifier')        
    # )
    email = LowercaseEMailField(_('email address'), blank=True, null=True)
    username = LowercaseUsernameField(
        _('username'), 
        unique=True,
        max_length=150,
        validators=[username_validator],
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists.")
        },
    )
    name = models.CharField(
        _('name'), 
        max_length=255,
        blank=True,
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    

    following = models.ManyToManyField(
        'User',
        through='Contact',
        related_name='followers',
        symmetrical=False,
        verbose_name=_('following')
    )



    USERNAME_FIELD = ('username')
    REQUIRED_FIELDS = ['email']
    EMAIL_FIELD = 'email'

    objects = CustomeUserManager()

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('user_detail', args=[self.username])

    

class Contact(models.Model):
    user_from = models.ForeignKey(
        User,
        related_name='rel_from_set',
        on_delete=models.CASCADE,
    )
    user_to = models.ForeignKey(
        User,
        related_name='rel_to_set',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'
