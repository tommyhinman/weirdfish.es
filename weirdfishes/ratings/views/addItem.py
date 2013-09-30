from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from ratings.models import Artist, Item, Rating

@login_required
def addItem(request):
	user = request.user
	artist = Artist.objects.get( pk=request.POST['artist_id'] )
	name = request.POST['item_name']
	itemType = request.POST['item_type']
	releaseDate = request.POST['release_date']

	item = Item( artist=artist, name=name, release_date=releaseDate, item_type=itemType)
	item.save()
	itemId = item.pk

	return HttpResponseRedirect(reverse('ratings:viewArtist', args=(artist.id,)))

