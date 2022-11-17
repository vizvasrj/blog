from django.utils.translation import gettext as _

from django import forms 
from .models import Post
from django.utils import dateformat, timezone
from django.utils.timezone import localtime

lt = localtime(timezone.now())


fomated_time = dateformat.format(lt, 'Y-m-d H:i')


class PostForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Publish')),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'myfieldclass bg-red-lite'}))

    class Meta:
        model = Post
        fields = (
            'title', 'body', 'cover', 'status', 'publish',
            # 'category',
        )
        widgets = {
            'title': forms.Textarea(
                attrs={'class': 'myfieldclass padding-15 border-bottom', 'autocomplete': 'off',
                'rows': "2", 'placeholder': _('Title')}
            ),
            'body': forms.Textarea(
                # config={'minHeight': 100}
                attrs={
                'placeholder': _('Type content here.'),
                    'class': 'myfieldclass ',
                }
            ),
            'cover': forms.FileInput(
                attrs={
                    'class': 'myfieldclass',
                    'required': False
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'bg-red',
                }
            ),

            
        }
