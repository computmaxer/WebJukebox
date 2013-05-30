from webjukebox import models, utils

from django.contrib.auth.models import User

from datetime import datetime



def get_events_for_user(user):
#    event_ids = user.profile.associated_events
    associated_events = []
    events = models.Event.objects.all()
    for event in events:
        if user.id in event.admin_keys:
            associated_events.append(event)
    return associated_events


def create_event(data, user):
    event = models.Event(**data)
    event.creator = user
    event.admin_keys = [user.id]
    event.save()
    user.profile.associated_events.append(event.id)
    user.profile.save()
    return event


def get_event(event_id):
    return models.Event.objects.get(id__exact=event_id)
    

def get_nearby_events(zipcode):
    hi_zip = zipcode + 50
    low_zip = zipcode - 50
    events = models.Event.objects.filter(zipcode__lt = hi_zip).filter(zipcode__gt = low_zip)
    return events


def create_user(data):
    #write function to create user
    user = models.User(
        username=data.get('username'),
        email =  data.get('email'),
        first_name = "",
        last_name = "")
    user.save()
    user.set_password(data.get('password'))
    user.save()
    user.profile.is_dj = data.get('is_dj')
    user.profile.streetaddress = ""
    user.profile.city = ""
    user.profile.zipcode = 0
    user.profile.save()
    
    return user

def update_user(data,user):
    #function to update user data
    
    #Check currently logged in user to see if the username field
    #matches with it. If it does the skip the try,except block.
    if (user.username!=data.get('username')):
        try:
            User.objects.get(username=data.get('username'))
        except User.DoesNotExist:
            #This means that the new username is valid.
            user.username = data.get('username')
            user.first_name = data.get('firstname')
            user.last_name = data.get('lastname')
            profile = user.profile
            profile.streetaddress = data.get('streetaddress')
            profile.city = data.get('city')
            profile.zipcode = data.get('zipcode')
            profile.is_dj = data.get('is_dj')
            profile.save()
            user.save()
            return
        
        
        
    else:
        user.first_name = data.get('firstname')
        user.last_name = data.get('lastname')
        profile = user.profile
        profile.streetaddress = data.get('streetaddress')
        profile.city = data.get('city')
        profile.zipcode = data.get('zipcode')
        profile.is_dj = data.get('is_dj')
        profile.save()
        user.save()


def get_library_by_id(library_id):
    return models.Library.objects.get(id__exact=library_id)
    
def edit_library(data):
    library = get_library_by_id(data.get('library'))
    library.name = data.get('name')
    library.save()

def get_libraries_for_user(user):
    libraries = models.Library.objects.filter(owner = user)
    return libraries

def delete_library(library_id):
    library = get_library_by_id(library_id)
    library.delete()

def read_library_file_upload(data, user):
    library = models.Library()
    library.name = data.get('name', "My Library Name")
    library.owner = user
    f = data.get('file', None)
    if f:
        keys = parse_playlist_file(f, library)
        library.song_count = 0
        for key in keys:
            library.add_song(key)
                    
        library.save()
        return library
    
    else:
        raise Exception("Failed to upload file")
    
def parse_playlist_file(f, library):
    keys = []
    song_list = utils.parse_playlist(f)
    for line in song_list:
        song = models.Song()
        song.title = line['title']
        song.artist = line['artist']
        song.album = line['album']
        song.minutes = line['minutes']
        song.seconds = line['seconds']
        song.library = library.name
        song.save()
        keys.append(song.id)
    return keys

def get_libraries_by_event(event):
    library_ids = event.library_keys
    libraries = models.Library.objects.filter(id__in=library_ids)
    return list(libraries)

def request_song(event, song_id, action='add'):
    ret_string = 'none'
    song = models.Song.objects.get(id__exact=song_id)
    request = models.Request.objects.filter(event=event).filter(song=song)
    if action == 'add':
        if request:
            request = request[0]
            request.count +=1
            request.last_requested = datetime.now()
            if request.status == models.Request.PLAYED_STATUS:
                request.status = models.Request.REQUESTED_AGAIN_STATUS
        else:
            request = models.Request(event=event, song=song, count=1,
                                     last_requested=datetime.now(),
                                     status=models.Request.UNPLAYED_STATUS)
        ret_string = 'added'
    elif action == 'remove':
        if not request:
            return ret_string
        else:
            request = request[0]
            request.count = request.count - 1
            ret_string = 'removed'
    request.save()
    return ret_string

def update_request_status(request_id, action):
    ret_string = 'none'
    request = models.Request.objects.filter(id__exact=request_id)
    if request:
        request = request[0]
        if action == 'play':
            request.status = models.Request.PLAYED_STATUS
        elif action == 'nope':
            request.status = models.Request.NEVER_PLAY_STATUS
        request.save()
        ret_string = 'success'
    return ret_string

def get_song_requests_for_event(event):
    requests = list(models.Request.objects.filter(
        event=event).filter(status__lt=models.Request.PLAYED_STATUS))
    ret_requests = []
    for request in requests:
        if request.count > 0:
            ret_requests.append(request)
    return ret_requests

def get_all_event_requests(event):
    return list(models.Request.objects.filter(event=event))

def get_artist_stats(event):
    all_requests = get_all_event_requests(event)
    artist_dict = {}
    for request in all_requests:
        if request.song.artist and request.song.artist != '' or ' ':
            if request.song.artist not in artist_dict:
                artist_dict[request.song.artist] = request.count
            else:
                artist_dict[request.song.artist] += request.count
    return artist_dict

