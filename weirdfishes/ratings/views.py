from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from auth import GoogleBackend

from ratings.models import Artist, Item, Rating

@login_required
def index(request):
	#if not request.user.is_authenticated():
	#	return redirect('/google/login/?next=%s' % request.path)

	artistList = Artist.objects.all()
	user = request.user
	context = {'artistList' : artistList, 'user': user}
	return render(request, 'ratings/index.html', context)

@login_required
def viewArtist(request, artist_id):
	artist = get_object_or_404(Artist, pk=artist_id)
	itemList = Item.objects.filter(artist=artist)
	context = {'artist': artist, 'itemList': itemList}
	return render(request, 'ratings/viewArtist.html', context)

@login_required
def viewItem(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	artist = item.artist
	ratingList = Rating.objects.filter(item=item)
	context = {'artist': artist, 'item': item, 'ratingList': ratingList}
	return render(request, 'ratings/viewItem.html', context)

@login_required
def rateItem(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	value = request.POST['value']
	user = request.user

	# Update the rating if it exists, otherwise create it
	try:
		rating = Rating.objects.get( user=user, item=item )
		rating.value = value
	except (Rating.DoesNotExist):
		rating = Rating( user=user, item=item, value=value )

	rating.save()

	return HttpResponseRedirect(reverse('ratings:viewItem', args=(item.id, )))

# @login_required
# def addItem(request, artist_id):
# 	artist = get_object_or_404(Artist, pk=artist_id)
# 	name = request.POST['name']
# 	itemType = request.POST['type']

	
