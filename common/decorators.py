from django.http import HttpResponseBadRequest
from common.utils import is_ajax

from functools import wraps
from django.http import HttpResponseRedirect

def ajax_required(f):
    @wraps(f) #addred new [1]
    def wrap(request, *args, **kwargs):
        if not is_ajax(request=request):
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    # wrap.__doc__=f.__doc__ # [1]
    # wrap.__name__=f.__name__ # [1]
    return wrap




def authors_only(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):

        profile = request.user
        if profile.is_superuser:
             return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

  return wrap
