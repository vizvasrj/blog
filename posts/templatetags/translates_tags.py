from django import template

register = template.Library()

@register.filter(is_safe=True, name='tem_tags')
def tem_tags(post, language):
    # from termcolor import colored
    # print(colored('colored Val', 'red'))
    # print(colored(post, 'yellow'))
    # print(colored(language, 'magenta'))
    from blog.tblog.utils import get_tpost_ttags
    t_tags = get_tpost_ttags(is_post=post, need_tags=True, language=language)
    return t_tags


@register.filter(is_safe=True, name='tr_post')
def tr_post(post, language):
    from blog.tblog.utils import get_tpost_ttags
    t_post = get_tpost_ttags(is_post=post, language=language, need_post=True)
    return t_post


@register.filter(is_safe=True, name='short')
def short(body, ln):
    if ln in ('ko', 'ja', 'zh-hans'):
        body = body[:100]
    else:
        body = ' '.join(body.split(' ')[:100])
    return body

@register.filter(is_safe=True, name='lname')
def lname(lan):
    if lan == 'en':
        return 'English'
    elif lan == 'ar':
        return 'العربيّة'
    elif lan == 'zh-hans':
        return '简体中文'
    elif lan == 'tl':
        return 'Filipino'
    elif lan == 'fr':
        return 'français'
    elif lan == 'de':
        return 'Deutsch'
    elif lan == 'hi':
        return 'हिंदी'
    elif lan == 'id':
        return 'Bahasa Indonesia'
    elif lan == 'it':
        return 'italiano'
    elif lan == 'ja':
        return '日本語'
    elif lan == 'ko':
        return '한국어'
    elif lan == 'nn':
        return 'norsk (nynorsk)'
    elif lan == 'pt':
        return 'Português'
    elif lan == 'ru':
        return 'Русский'
    elif lan == 'es':
        return 'español'
    elif lan == 'vi':
        return 'Tiếng Việt'
    elif lan == 'bn':
        return 'বাংলা'
    elif lan == 'mr':
        return 'मराठी'
    elif lan == 'te':
        return 'తెలుగు'
    elif lan == 'ta':
        return 'தமிழ்'
    elif lan == 'gu':
        return 'ગુજરાતી'
    elif lan == 'ur':
        return 'اردو'
    elif lan == 'kn':
        return 'ಕನ್ನಡ'
    elif lan == 'or':
        return 'ଓଡିଆ'
    elif lan == 'ml':
        return 'മലയാളം'
    elif lan == 'pa':
        return 'ਪੰਜਾਬੀ'
    else:
        return 'English'

# from django.core.exceptions import ObjectDoesNotExist

# @register.filter(is_safe=True, name='editnon')
# def editnon(post, ln):
#     from mytag.utils import classmap_post
#     try:
#         classmap_post[f'{ln}_post'].objects.get(post=post)
#     except ObjectDoesNotExist:
#         return True