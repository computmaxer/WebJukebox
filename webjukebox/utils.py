from django.conf import settings
from django.template import RequestContext
import re

def get_context(request):
    context = {}

    if request.user:
        context['user'] = request.user
    if 'song-requests' not in request.session:
        request.session['song-requests'] = ['-1']

    r_ctx = RequestContext(request, context)
    return r_ctx


def get_event_context(request, **kwargs):
    import actions
    context = get_context(request)
    event_id = kwargs.get('event_id', None)
    context['event'] = actions.get_event(event_id)

    return context

def parse_m3u(contents):
    song_list = []
    for line in contents.splitlines():
        if '#EXTINF:' in line:
            title_artist = line[line.index(',') + 1:]
            fields = title_artist.split(' - ')
            title = fields[0]
            artist = fields[1]
            song_list.append({'title':title, 'artist':artist, 'album':"", 'minutes':0, 'seconds':0})
    return song_list

def parse_itunes_txt(contents):
    song_list = []
    firstline = True
    for line in contents.splitlines():
        if firstline:
            firstline = False
        elif line:
            fields = line.split('\t')
            title = fields[0]
            artist = fields[1]
            album = fields[3]
            time = fields[7] or 0
            song_list.append({'title':title, 'artist':artist, 'album':album, 'minutes':(int(time)/60), 'seconds':(int(time)%60)})
    return song_list
import codecs
def parse_playlist(f):
    song_list = []
    contents = ""
    for chunk in f.chunks():
        try:
            contents += unicode(chunk,'utf-16').encode('ascii','ignore')
        except:
            contents += chunk

    first_line = contents.splitlines()[0]

    if '#EXTM3U' in first_line:
        song_list = parse_m3u(contents)
    elif 'Artist' in first_line:
        song_list = parse_itunes_txt(contents)
    else:
        raise Exception("Could not determine file type!")
        
    return song_list
