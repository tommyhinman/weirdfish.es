from django.conf.urls import patterns, url

from ratings import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
