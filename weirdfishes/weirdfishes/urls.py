from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

from django.conf import settings
from django.contrib import admin
admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
url(r'^admin/', include(admin.site.urls)),

#authentication urls
url(r'^login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
url(r'logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/',}, name='logout'),

url(r'^polls/', include('polls.urls', namespace="polls")),
url(r'^', include('ratings.urls', namespace="ratings")),

url(r'^%s' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
