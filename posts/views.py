from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from termcolor import colored
from django.utils import timezone
import pytz
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Image
import os
import requests
from django.core.files import File

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from common.decorators import is_ajax
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django import http
# Create your views here.

def delta_time(time):
    delta = time + timezone.timedelta(minutes=1)
    if delta >= timezone.localtime(timezone.now()):
        return time
    else:
        return timezone.localtime(timezone.now())


def cover2_upload(url, creator_url, creator_name):
    timestamp = datetime.now().timestamp()
    imgname = f'{timestamp}.jpg'
    try:
        r = requests.get(url).content
        with open(imgname, 'wb') as f:
            f.write(r)
        fileimg = File(open(imgname, 'rb'))
        image = Image.objects.create(
            image=fileimg, 
            creator_url=creator_url,
            creator_name=creator_name
        )
        os.remove(imgname)

        return image
    except:
        return None



@login_required
def create_post(request):
    
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        try:
            cover = request.FILES.get('cover')
            title = request.POST.get('title')
            body = request.POST.get('body')
            status = request.POST.get('status')
            print(colored(request.POST, 'red'))
            print(colored(cover, 'blue'))
        except:
            return render(
                request,
                'posts/post_form.html', {
                    'form': form,
                }
            )

        
        post = Post.objects.create(
            title=title,
            body=body,
            status=status,
            author=request.user
        )
        post.cover = cover
        post.save()

        return redirect(post.get_absolute_url())


    else:
        form = PostForm(data=request.POST, files=request.FILES)
    return render(
        request,
        'posts/post_form.html', {
            'form': form,
        }
    )







def post_list(request):
    # print('\n\n',request.META.get('HTTP_REFERER'))
    # posts = Post.published.all()
    posts = Post.published.all().order_by('-updated')
    # print(translation.get_language_from_request(request))
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
    return render(
        request,
        'posts/list.html', {
            'posts': posts,

        }
    )

def post_detail(request, slug):

    try:
        post = Post.objects.get(slug=slug)


        # print(post, "aaa"*100)
    except Post.DoesNotExist:
        return HttpResponse("404")
    
    if post.status == "draft":
        
        if post.author != request.user:
            return HttpResponse("THis Is un published")
    return render(
        request,
        'posts/detail.html', {
            "post": post
        }    
    )

from django.http import JsonResponse

@login_required
def date_ajax_get(req):
    # if req.method == 'POST':
    mytime = (timezone.now().astimezone(pytz.timezone(settings.mytimezone))+timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M')
    # tmy = timezone.datetime.strptime(f'{mytime} {tz}', '%Y-%m-%d %H:%M %z')

    # from zoneinfo import ZoneInfo
    # date = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=5)
    # date_str = date.strftime('%Y-%m-%d %H:%M')
    # date_str = tmy.strftime('%Y-%m-%d %H:%M')

    return JsonResponse({'status': 'ok', 'date': mytime})  

from django.utils.translation import gettext as _

@login_required
@ajax_required
@require_POST
def date_check_past(req):
    if req.method == 'POST':
        publish = req.POST.get('publish')
        # tz = req.POST.get('tz')
        try:
            tmy = timezone.datetime.strptime(f'{publish}', '%Y-%m-%d %H:%M')
            # tmy = timezone.datetime.strptime(f'{publish} {tz}', '%Y-%m-%d %H:%M %z')
            # t = tmy.astimezone(pytz.timezone('UTC'))
            # from termcolor import colored
            # print(colored(tmy, 'red'))
            # d_with_tz = timezone.datetime(year=t.year, month=t.month, day=t.day, hour=t.hour, minute=t.minute, tzinfo=pytz.UTC)
            # print('my to utc', d_with_tz)
            # print('now utc', timezone.now())
            # naive = t.replace(tzinfo=None)
            # humanize.activate(req.LANGUAGE_CODE)
            # message = humanize.naturaltime(naive)
            tnow = timezone.now().astimezone(pytz.timezone(settings.mytimezone))
            tnow2 = tnow.replace(tzinfo=None)
            # print(colored(tnow2, 'blue'))
            if tmy < tnow2:
                return JsonResponse({'status': 'ok', 'message': _("Please check your system's date. Its may be incorrect or You are entering date in past.")})

            else:
                return JsonResponse({'status': 'ok', 'message': _('It will be published at given time')})
        except :
            return JsonResponse({'status': 'ok', 'message': _('Wrong Formate, Correct are "YYYY-MM-DD HH:MM"')})




@login_required
def update_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return HttpResponse("404")
    
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        try:
            cover = request.FILES.get('cover')
            title = request.POST.get('title')
            body = request.POST.get('body')
            status = request.POST.get('status')
            # print(colored(request.POST, 'red'))
            # print(colored(cover, 'blue'))
        except:
            return render(
                request,
                'posts/post_form.html', {
                    'form': form,
                }
            )
        
        post.title=title
        post.body=body
        post.status=status
        if cover != None: 
            # print(colored(post.cover, 'green'))
            
            post.cover = cover
        

        post.save()

        return redirect(post.get_absolute_url())

    

    else:
        data = {
            "title": post.title,
            "body": post.body,
            "status": post.status,
        }
        files = {
            "cover": post.cover

        }
        form = PostForm(data=data, files=request.FILES, instance=post)
    if post.cover:
        imgcover = post.cover.url
    else:
        imgcover = None
    return render(
        request,
        'posts/post_form.html', {
            'form': form,
            "imgcover": imgcover
        }
    )

from .models import Category

@login_required
def category_list(request):
    posts = Category.objects.filter(created_by=request.user).order_by('-updated')
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
            'posts/category/list_ajax.html', {
                'posts': posts,
            }
        )
    return render(
        request,
        'posts/category/list.html', {
            'posts': posts,

        }
    )

@login_required
def delete_category(request, slug):
    try:   
        

        post = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return HttpResponse("404")
    if post.created_by != request.user:
        return HttpResponse("401 Unauthorized")
    post.delete()
    return http.HttpResponseRedirect(reverse('category_list'))


@login_required
def delete_post(request, slug):
    try:   
        

        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return HttpResponse("404")
    if post.author != request.user:
        return HttpResponse("401 Unauthorized")
    post.delete()
    return http.HttpResponseRedirect(reverse('dashboard'))


@login_required
def unpublish_post(request, slug):
    try:   
        

        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return HttpResponse("404")
    if post.author != request.user:
        return HttpResponse("401 Unauthorized")
    post.status = "draft"
    post.save()
    return http.HttpResponseRedirect(reverse('dashboard'))


@login_required
def publish_post(request, slug):
    try:   
        

        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return HttpResponse("404")
    if post.author != request.user:
        return HttpResponse("401 Unauthorized")
    post.status = "published"
    post.save()
    return http.HttpResponseRedirect(reverse('dashboard'))
