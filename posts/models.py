from django.db import models
from django.urls import reverse
from users.models import User
from django.utils.translation import gettext as _
from django.utils import timezone
from accounts.models import Profile

class Image(models.Model):
    image = models.ImageField(
        _('cover'),
        upload_to='cover/%Y/%m/%d',
        blank=True, null=True
        )  
    creator_name = models.CharField(
        _('photographer name'),
        max_length=100,
        blank=True, null=True
    )
    creator_url = models.CharField(
        _('photographer profile url'),
        max_length=100,
        blank=True, null=True
    )
    sha_256 = models.CharField(
        _('sha_256'),
        max_length=64,
        blank=True, null=True, 
        db_index=True
    )
    def __str__(self):
        return self.image


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=150)
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='users_category',

    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='parents_categories',
        blank=True, null=True
    )
    
    is_public = models.BooleanField(default=False)

    def __str__(self):
        if self.parent:
            return f'{self.parent} > {self.name}'
        return self.name

class ActiveUserPublishedManager(models.Manager):
    def get_queryset(self):
        return super(ActiveUserPublishedManager, self).get_queryset().filter(
            author__is_active=True
        ).filter(publish__lte=timezone.now()).filter(
            status='published'
        )



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(
            PublishedManager, self
        ).get_queryset().filter(
            # publish__lte=now
            status='published'
        )



class DraftedManager(models.Manager):
    def get_queryset(self):
        return super(
            DraftedManager, self
        ).get_queryset().filter(
            status='draft'
        )


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
    )
    title = models.CharField(_('title'), max_length=256)
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name=_('category')
    )
    cover = models.ImageField(
        _('cover'),
        upload_to='cover/%Y/%m/%d',
        blank=True, null=True
    )
    cover2 = models.ForeignKey(
        Image,
        on_delete=models.DO_NOTHING,
        related_name='im_posts',
        blank=True, null=True,
        verbose_name=_('cover image')
    )
    slug = models.CharField(max_length=256, blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name=_('author')
    )
    body = models.TextField()
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    updated = models.DateTimeField(db_index=True, auto_now=True)
    # publish = models.DateTimeField(default=timezone.now)
    publish = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='published'
    )
    objects = models.Manager()
    published = PublishedManager()
    aupm = ActiveUserPublishedManager()
    drafted = DraftedManager()
    users_like = models.ManyToManyField(
        User,
        related_name='posts_liked',
        blank=True
    )
    bookmark_list = models.ManyToManyField(
        User,
        related_name='post_bookmark',
        blank=True
    )
    total_likes = models.PositiveIntegerField(
        db_index=True,
        default=0
    )
    
    class Meta:
        ordering = ('-publish',)
        get_latest_by = ['id']


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # activate('hi')

        return reverse("post_detail", kwargs={"slug": self.slug })
    
    def get_update_url(self):
        # activate('hi')

        return reverse("update_post", kwargs={"slug": self.slug })
    
    def get_delete_url(self):
        # activate('hi')

        return reverse("delete_post", kwargs={"slug": self.slug })

    def get_unpublish_post_url(self):
        # activate('hi')

        return reverse("unpublish_post", kwargs={"slug": self.slug })


    def get_publish_post_url(self):
        # activate('hi')

        return reverse("publish_post", kwargs={"slug": self.slug })

