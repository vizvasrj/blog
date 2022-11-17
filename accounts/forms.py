from django import forms
from django.utils.translation import gettext as _
from users.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), widget=forms.PasswordInput(attrs={
        'class': 'myfieldclass2',
        'placeholder': _('Username'),
        'type': 'text',
        'name': 'username'
    }))

    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={
        'class': 'myfieldclass2',
        'placeholder': _('Password'),
        'type': 'password',
        'name': 'password'
    }))


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={
        'class': 'myfieldclass2',
        'placeholder': _('Password ...'),
        'type': 'password',
        'name': 'password'
    }))
    password2 = forms.CharField(label=_('Repeat Password'), widget=forms.PasswordInput(attrs={
        'class': 'myfieldclass2',
        'placeholder': _('Repeat Password ...'),
        'type': 'password',
        'name': 'password'
    }))
    username = forms.CharField(label=_('Username'), widget=forms.TextInput(attrs={
        'class': 'myfieldclass2',
        'placeholder': _('Username ...'),
        'type': 'text',
        'name': 'username'
    }))

    email = forms.CharField(label=_('Email'), widget=forms.EmailInput(attrs={
        'class': 'myfieldclass2 ',
        'placeholder': _('Email ...'),
        'type': 'email',
        'name': 'email'
    }))



    class Meta:
        model = User
        fields = ('username', 'email')
        
        help_texts = {
            'username': '',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(
                _("Passwords doesn't Matched."))
        return cd['password2']

from .models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        models = Profile
        fields = (
            'photo',
        )
