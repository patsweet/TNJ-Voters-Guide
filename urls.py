from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'VotersGuide.views.home', name='home'),
    # url(r'^VotersGuide/', include('VotersGuide.foo.urls')),
    
    # Matchmaker URLS
    url(r'^matchmaker/$', 'matchmaker.views.index'),
    url(r'^matchmaker/(?P<Race_id>\d+)/$', 'matchmaker.views.race_page'),
    url(r'^matchmaker/(?P<Race_id>\d+)/(?P<Candidate_id>\d+)/$', 'matchmaker.views.candidate_page'),
    url(r'^matchmaker/(?P<Race_id>\d+)/match_game/$', 'matchmaker.views.matchmaker_game'),

    # Registration / Login / Etc.
    url(r'^matchmaker/logout/$', 'matchmaker.views.logout_page'),
    url(r'^matchmaker/login/$', 'django.contrib.auth.views.login'),
    url(r'^matchmaker/change_password/$', 'django.contrib.auth.views.password_change'),
    url(r'^matchmaker/password_change_successful/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^matchmaker/update/$', 'matchmaker.views.update_page'),
    url(r'^matchmaker/answer/$', 'matchmaker.views.update_answers'),
                       
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
   )