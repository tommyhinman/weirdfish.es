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
    url(r'^item/(?P<item_id>\d+)/rate/$', views.rateItem, name='rateItem'),

    #Add Item /addItem
    url(r'^addItem/$', views.addItem, name='addItem'),

    #Delete Item /deleteItem
    url(r'^item/(?P<item_id>\d+)/deleteItem/$', views.deleteItem, name='deleteItem'),

    #Add Artist /addArtist
    url(r'^addArtist/$', views.addArtist, name='addArtist'),

    #View User /viewUser/123
    url(r'^viewUser/(?P<user_id>\d+)/$', views.viewUser, name='viewUser'),

    #View All Users /viewAllUsers
    url(r'^viewAllUsers/$', views.viewAllUsers, name='viewAllUsers'),

    #Search
    url(r'^search', views.search, name='search'),
)
