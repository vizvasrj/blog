# from django.shortcuts import render
import functools
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _
from django.core.validators import validate_email as validateEmail
from django.core.exceptions import ValidationError
from users.models import User
from django.contrib.auth.decorators import login_required
from posts.models import Post


def logged_in_user_redirect(function):
    @functools.wraps(function)
    def wrap(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect(reverse('post_list'))
        else:
            return function(request, *args, **kwargs)
    # wrap.__doc__ = function.__doc__
    # wrap.__name__ = function.__name__
    return wrap


# Create your views here.
@logged_in_user_redirect
def user_login(request):
    captcha = True
    message = None
    next = None
    if request.GET:
        next = request.GET.get('next')
    if settings.HOME_DOMAIN == 'http://127.0.0.1:8000':
        captcha = False

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if True:
        # if recaptcha(request):
            pass
        else:
            message = _('Captcha is invalid.')
            return render(
                request,
                'accounts/login.html', {
                    'form': form,
                    'message': message,
                    'captcha': captcha,
                    'next': next,
                }
            )
        if form.is_valid():
            cd = form.cleaned_data
            user_k = cd['username']
            pass_k = cd['password']
            user = authenticate(
                request,
                username=user_k,
                password=pass_k
            )
            if user == None:
                message = _('User does not exist or password is not matched')
                return render(
                    request,
                    'accounts/login.html', {
                        'form': form,
                        'message': message
                    })

            if user.is_deleted == True:
                return HttpResponseRedirect(reverse('account_deletion_status'))

            elif next:
                print("here")
                print(user)
                login(request, user,
                      backend='accounts.authentication.EmailAuthBackend')
                print("After here")
                return HttpResponseRedirect(next)

            elif user.last_login and user.is_active == True:
                login(request, user,
                      backend='accounts.authentication.EmailAuthBackend')
                return HttpResponseRedirect(reverse('dashboard'))

            elif user.last_login == None:
                login(request, user,
                      backend='accounts.authentication.EmailAuthBackend')
                return HttpResponseRedirect(reverse('dashboard'))

    form = LoginForm(request.POST)

    return render(
        request,
        'accounts/login.html', {
            'form': form,
            'message': message,
            'captcha': captcha,
            'next': next,
        }
    )


def register(request):
    captcha = False
    from termcolor import colored
    if request.user.is_authenticated:
        return redirect(reverse('post_list'))
    else:
        if request.method == 'POST':
            # print(colored(request.POST, 'red'))
            if settings.HOME_DOMAIN == 'http://127.0.0.1:8000':
                pass
            else:
                pass
            data = request.POST
            email = data.get('email')
            password1 = data.get('password1')
            password2 = data.get('password2')
            username = data.get('username')
            try:
                validateEmail(email)
            except ValidationError:
                return JsonResponse({'status': 'ok', 'message': _('Email Is Not validated. ')})
            if not (username and email and password1 and password2):
                return JsonResponse({'status': 'ok', 'message': _('Please fill all fields. ')})
            if not len(username) > 0:
                return JsonResponse({'status': 'ok', 'message': _('Username must not be empty.'), 'type': 'username'})
            
            non_valid_character = '<>@&;"\'?`/'
            valid = True
            for x in username:
                if x in non_valid_character:

                    valid = False
            if valid == False:
                return JsonResponse({'status': 'ok', 'message': _(f'Username must not contain these characters. {non_valid_character}'), 'type': 'username'})
                    
            if password1 != password2:
                return JsonResponse({'status': 'ok', 'message': _('Repeated password did not matched.')})

            # ! Checking Users email or Username is already register or not
            cuser = User.objects.filter(username=username).exists()
            cemail = User.objects.filter(email=email).exists()
            if cuser:
                return JsonResponse({'status': 'ok', 'message': _('username Is already register with us.'), 'type': 'username'})
            if cemail:
                return JsonResponse({'status': 'ok', 'message': _('Email Is already register with us.'), 'type': 'email'})

            # ! Creating User her
            user = User.objects.create(
                username=username,
                email=email,
            )
            user.is_active = True
            user.set_password(password1)
            user.save()
            # Profile.objects.create(user=user, lang=language, timezone=timezone)
            # return render(
            #     request,
            #     'accounts/register_done.html',
            #     {'new_user': user}
            # )
            return JsonResponse({'status': 'ok', 'message': _('You have created account, '), 'type': 'success'})

            # try:
            #     user_exists = User.objects.get(username=request.POST['username'])
            #     return JsonResponse({'status': 'ok', "message":_("User already exists")}, status=200)
            # except User.DoesNotExist:
            #     # pass
            #     if user_form.is_valid():
            #         new_user = user_form.save(commit=False)
            #         new_user.set_password(
            #             user_form.cleaned_data['password1']
            #         )
            #         print(new_user)
            #         print(colored(request.POST, 'red'))
            #         return JsonResponse({'status': 'ok', 'message': 'Some Message'})
            # new_user.save()
            # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            # try:
            #     ip = x_forwarded_for.split(',')[0]
            #     import requests
            #     data = requests.get('http://ip-api.com/json/'+ip).json()
            #     timezone_str = data['timezone']
            #     from .timezone import from_user
            #     timezone = from_user[timezone_str]

            # except:
            #     timezone = 462
            # Profile.objects.create(user=new_user, lang=language, timezone=timezone)
            # return render(
            #     request,
            #     'accounts/register_done.html',
            #     {'new_user': new_user}
            # )
        else:
            user_form = UserRegistrationForm()
        return render(
            request,
            'accounts/register.html',
            {'user_form': user_form, 'captcha': captcha}
        )


@login_required
def dashboard(request):
    try:
        
        posts = Post.objects.filter(author=request.user).order_by('-updated')
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            if is_ajax(request=request):
                return HttpResponse('')
            posts = paginator.page(paginator.num_pages)
        if is_ajax(request=request):
            print("ajax")
            return render(
                request,
                'accounts/post/list_ajax.html', {
                    'posts': posts,
                    "dashboard": True
                }
            )
    except User.DoesNotExist:
        return HttpResponse("404")
    return render(
        request,
        'accounts/user_detail.html', {
            "posts": posts,
            "dashboard": True
        }
    )
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from common.decorators import is_ajax

def user_detail(request, slug):
    try:
        user = User.objects.get(username=slug)
        posts = Post.published.filter(author=user).order_by('-updated')
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            if is_ajax(request=request):
                return HttpResponse('')
            posts = paginator.page(paginator.num_pages)
        if is_ajax(request=request):
            return render(
                request,
                'posts/list_ajax.html', {
                    'posts': posts,
                }
            )
    except User.DoesNotExist:
        return HttpResponse("404")
    return render(
        request,
        'accounts/user_detail.html', {
            "user": user,
            "posts": posts
        }
    )

from .forms import ProfileEditForm
from .models import Profile

@login_required
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if profile.photo:
        myphoto = profile.photo.url
    photo = request.FILES.get('photo')
    from termcolor import colored
    print(colored(photo, 'red'))
    print(colored(request.POST, 'blue'))
    print(colored(request.FILES, 'green'))

    if photo:
        profile.photo = photo
        profile.save()
        
    
    return render (
        request,
        'accounts/profile.html', {
            "myphoto": myphoto
        }
    )