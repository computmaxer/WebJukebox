from django.conf.urls.defaults import *
from django.contrib import admin

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    # gae
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),

    # django admin and login
    (r'^admin/', include(admin.site.urls)),

    # # # # # # Base pages # # # # # #
    url(r'^$', 'webjukebox.views.patron.index', name='site-index'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='site-login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='site-logout'),
    url(r'^register/$', 'webjukebox.views.patron.registration', name='account-registration'),


    # # # # # # DJ Pages # # # # # #
    url(r'^dj/events/$', 'webjukebox.views.dj.select_event', name='select-event'),
    url(r'^dj/events/(?P<event_id>[0-9-_:]+)/requests/$', 'webjukebox.views.dj.event_requests', name='dj-event-requests'),
    url(r'^dj/events/(?P<event_id>[0-9-_:]+)/displays/$', 'webjukebox.views.dj.event_displays', name='dj-event-displays'),
    url(r'^dj/events/(?P<event_id>[0-9-_:]+)/statistics/$', 'webjukebox.views.dj.event_statistics', name='dj-event-statistics'),
    url(r'^dj/events/(?P<event_id>[0-9-_:]+)/settings/$', 'webjukebox.views.dj.event_setup', name='dj-event-setup'),
    url(r'^dj/events/(?P<event_id>[0-9-_:]+)/library/(?P<library_id>[0-9-_:]+)/$', 'webjukebox.views.dj.event_libraries_setup', name='dj-event-libraries-setup'),
    url(r'^dj/events/(?P<event_id>[0-9-_:]+)/requests/status/$', 'webjukebox.views.dj.update_event_request_status', name='dj-event-request-status'),
    url(r'^events/(?P<event_id>[0-9-_:]+)/qrcode/$', 'webjukebox.views.dj.display_qrcode', name='event-qrcode'),
    
    url(r'^dj/account_settings/$', 'webjukebox.views.dj.account_settings', name='account-settings'),
    url(r'^dj/libraries/$', 'webjukebox.views.dj.view_libraries', name='view-libraries'),
    url(r'^dj/libraries/(?P<library_id>[0-9-_:]+)/songs/$', 'webjukebox.views.dj.view_songs_in_library', name='view-songs-in-library'),
    url(r'^dj/libraries/delete/$', 'webjukebox.views.dj.delete_library', name='delete-library'),


    # # # # # # Patron Pages # # # # # #
    url(r'^events/find/$', 'webjukebox.views.patron.find_event', name='find-event'),
    url(r'^events/(?P<event_id>[0-9-_:]+)/requests/$', 'webjukebox.views.patron.event_requests', name='patron-event-requests'),
    url(r'^events/(?P<event_id>[0-9-_:]+)/request/$', 'webjukebox.views.patron.request_song', name='patron-request-song')


    )
