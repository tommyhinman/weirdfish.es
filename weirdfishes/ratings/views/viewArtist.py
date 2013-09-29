from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from ratings.models import Artist, Item, Rating

@login_required
def viewArtist(request, artist_id):
	artist = get_object_or_404(Artist, pk=artist_id)
	itemList = Item.objects.filter(artist=artist)

	for item in itemList:
		ratingAverage = Rating.objects.filter(item=item).aggregate(Avg('value'))['value__avg']
		item.average_rating = round(ratingAverage)

	itemTypeList = Item.ITEM_TYPES

	context = {'artist': artist, 'itemList': itemList, 'itemTypeList': itemTypeList}
	return render(request, 'ratings/viewArtist.html', context)