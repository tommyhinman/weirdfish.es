from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from ratings.models import Artist, Item, Rating

@login_required
def viewArtist(request, artist_id):
	artist = get_object_or_404(Artist, pk=artist_id)
	itemList = Item.objects.filter(artist=artist)
	itemTypeList = Item.ITEM_TYPES

	context = {'artist': artist, 'itemList': itemList, 'itemTypeList': itemTypeList}
	return render(request, 'ratings/viewArtist.html', context)