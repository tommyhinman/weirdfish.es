from django.conf.urls import patterns, url

from ratings import views

urlpatterns = patterns('',
	#Main page
    url(r'^$', views.index, name='index'),

    #View Artist /artist/123
    url(r'^artist/(?P<artist_id>\d+)/$', views.viewArtist, name='viewArtist'),

    #View Item /item/456
    url(r'^item/(?P<item_id>\d+)/$', views.viewItem, name='viewItem'),

    #Rate item /item/456/rate
    url(r'^item/(?P<item_id>\d+)/rate/$', views.rateItem, name='rateItem')
)
