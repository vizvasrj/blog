from django.utils.safestring import mark_safe
from django import template
register = template.Library()

from bs4 import BeautifulSoup


def get_vimeo_id(url):
    from urllib.parse import urlparse
    query = urlparse(url)
    return query.path

def get_spotify_id(url):
    from urllib.parse import urlparse
    query = urlparse(url)
    return query.path

def get_daily_motion_video_id(url):
    from urllib.parse import urlparse, parse_qs
    
    query = urlparse(url)
    if 'dailymotion' in query.hostname:
        return (query.path).split('/')[2]
    else:
        raise ValueError




def get_yt_video_id(url):
    """Returns Video_ID extracting from the given url of Youtube
    
    Examples of URLs:
      Valid:
        'http://youtu.be/_lOT2p_FCvA',
        'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
        'http://www.youtube.com/embed/_lOT2p_FCvA',
        'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
        'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
        'youtube.com/watch?v=_lOT2p_FCvA',
      
      Invalid:
        'youtu.be/watch?v=_lOT2p_FCvA',
    """

    from urllib.parse import urlparse, parse_qs

    if url.startswith(('youtu', 'www')):
        url = 'http://' + url
        
    query = urlparse(url)
    
    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError

def youtube(watch_id):
    return f"""
        <div style="position: relative; padding-bottom: 100%; height: 0; padding-bottom: 56.2493%;">
            <iframe src="https://www.youtube.com/embed/{watch_id}"
                style="position: absolute; width: 100%; height: 100%; top: 0; left: 0;"
                frameborder="0" allow="autoplay; encrypted-media" allowfullscreen>
            </iframe>
        </div>
        """

def dailymotion(watch_id):
    return f"""
        <div style="position: relative; padding-bottom: 100%; height: 0; padding-bottom: 56.2493%;">
            <iframe src="https://www.dailymotion.com/embed/video/{watch_id}"
                style="position: absolute; width: 100%; height: 100%; top: 0; left: 0;"
                frameborder="0" allow="autoplay; encrypted-media" allowfullscreen>
            </iframe>
        </div>
        """
def soptify(long_hex_id):
    return f'''
    <iframe src="https://open.spotify.com/embed{long_hex_id}" width="100%"
     height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe> 
    '''

def vimeo(vimeo_video_id):
    return f'''
    <iframe src="https://player.vimeo.com/video{vimeo_video_id}"
     width="100%" height="360" frameborder="0" allow="autoplay; 
     fullscreen; picture-in-picture" allowfullscreen>
    </iframe>
    '''


def soups(html):
    soup = BeautifulSoup(html, 'html.parser')
    lists = []
    for x in soup:
        if x.name == 'script':
            lists.append(str(x).replace(
                '<',"&lt;").replace('>',"&gt;").replace(
                    '"', '&quot;').replace("'", '&#x27;'))
        if x.name == None:
            pass
        if x.name != 'script':
            if 'oembed url=' in str(x):
                # lists.append(str(x))
                pass
            else:
                lists.append(str(x))
        if x.name == 'figure':

            from urllib.parse import urlparse
            if 'https://' in str(x):
                url = str(x).split('"')[3]
            else:
                url = str(x).split('"')[2]
            query = urlparse(url)
            try:
                if 'youtu' or 'youtube' in query.hostname:
                        
                    try:
                        watch_id = get_yt_video_id(url)
                        lists.append(youtube(watch_id=watch_id))
                    except:
                        pass
                if 'daily' in query.hostname:
                    try:
                        watch_id = get_daily_motion_video_id(url)
                        # print(watch_id, "dailymotion")
                        lists.append(dailymotion(watch_id=watch_id))
                    except:
                        pass
                if 'spotify' in query.hostname:
                    try:
                        long_hex_id = get_spotify_id(url)
                        lists.append(soptify(long_hex_id=long_hex_id))
                    except:
                        pass
                if 'vimeo' in query.hostname:
                    try:
                        vimeo_video_id = get_vimeo_id(url)
                        lists.append(vimeo(vimeo_video_id=vimeo_video_id))
                    except:
                        pass
                else:
                    pass
            except:
                pass

    joined_html = ''.join(lists)

    # print(joined_html)
    return joined_html


@register.filter(is_safe=True, name='xssprotect')
def xssprotect(html):
    htmlone = soups(html)
    # print(htmlone)
    return mark_safe(htmlone)


import re
from lxml import etree
import lxml.html

@register.filter(is_safe=True, name='removeimage')
def removeimage(html):
    string = re.sub('<a.*?>|</a> ', ' ', html)
    string2 = re.sub('<img.*?>', ' ', string)
    return string2

@register.filter(is_safe=True, name='customestrip')
def customestrip(html_string):
    try:
        document = lxml.html.document_fromstring(html_string)
    except etree.ParseError:
        return html_string
    except etree.ParserError:
        return html_string
    d = " ".join(etree.XPath("//text()")(document))
    return re.sub(' +', ' ', d.replace('<', '&lt;').replace('>', '&gt;'))

