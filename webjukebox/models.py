from django.contrib.auth.models import User
from django.db import models
from djangotoolbox import fields as djtbx_fields


class Event(models.Model):
    name = models.CharField(max_length=60)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    creator = models.ForeignKey(User)
    admin_keys = djtbx_fields.ListField()
    library_keys = djtbx_fields.ListField()

    def has_library(self, library_id):
        if library_id in self.library_keys:
            return True
        return False


class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    minutes = models.IntegerField()
    seconds = models.IntegerField()
    library = models.CharField(max_length=60)

    def get_time(self):
        return "%i:%02i" % (self.minutes, self.seconds)

    def str_id(self):
        return str(self.id)


class Library(models.Model):
    name = models.CharField(max_length=60)
    owner = models.ForeignKey(User)
    song_keys = djtbx_fields.ListField()
    song_count = models.IntegerField()

    def add_song(self, key):
        self.song_keys.append(key)
        self.song_count += 1

    def get_songs(self):
        return list(Song.objects.filter(id__in=self.song_keys))

    def str_id(self):
        return str(self.id)


class Request(models.Model):
    event = models.ForeignKey(Event)
    song = models.ForeignKey(Song)

    count = models.IntegerField(default=1)
    last_requested = models.DateTimeField()

    UNPLAYED_STATUS = -1
    REQUESTED_AGAIN_STATUS = 0
    PLAYED_STATUS = 1
    NEVER_PLAY_STATUS = 2
    status = models.IntegerField(default=UNPLAYED_STATUS)


#Please keep this at the bottom of the file.  Add new classes above this.
class UserProfile(models.Model):
    user = models.ForeignKey(User)

    is_dj = models.BooleanField(default=False)
    streetaddress = models.TextField(default="")
    city = models.TextField(default="")
    zipcode = models.IntegerField(default=0)
    associated_events = djtbx_fields.ListField()

    def get_display_name(self):
        if self.user.first_name and self.user.last_name:
            return "%s %s" % (self.user.first_name, self.user.last_name)
        return self.user.username
    

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

""" LEAVE THIS COMMENTED OUT.
class User(models.Model):
"
Users within the Django authentication system are represented by this model.
Username and password are required. Other fields are optional.
"

    username = models.CharField(_('username'), max_length=30, unique=True, help_text=_("Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters"))
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True)
    password = models.CharField(_('password'), max_length=128, help_text=_("Use '[algo]$[salt]$[hexdigest]' or use the <a href=\"password/\">change password form</a>."))
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_("Designates whether the user can log into this admin site."))
    is_active = models.BooleanField(_('active'), default=True, help_text=_("Designates whether this user should be treated as active. Unselect this instead of deleting accounts."))
    is_superuser = models.BooleanField(_('superuser status'), default=False, help_text=_("Designates that this user has all permissions without explicitly assigning them."))
    last_login = models.DateTimeField(_('last login'), default=datetime.datetime.now)
    date_joined = models.DateTimeField(_('date joined'), default=datetime.datetime.now)
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True,
        help_text=_("In addition to the permissions manually assigned, this user will also get all permissions granted to each group he/she is in."))
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True)
"""