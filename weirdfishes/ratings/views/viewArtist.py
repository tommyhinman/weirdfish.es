from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from ratings.models import Artist, Item, Rating

@login_required
def viewArtist(request, artist_id):
	artist = get_object_or_404(Artist, pk=artist_id)
	itemList = Item.objects.filter(artist=artist)
	user = request.user

	for item in itemList:
		ratingAverage = Rating.objects.filter(item=item).aggregate(Avg('value'))['value__avg']
		item.inUsersList = Rating.objects.filter(user=user).filter(item=item).exists()

		if item.inUsersList:
			item.userRating = Rating.objects.filter(user=user).filter(item=item).get().value
		else:
			item.userRating = ""
		item.average_rating = round(ratingAverage) if (ratingAverage is not None) else 0

	itemTypeList = Item.ITEM_TYPES

	context = {'artist': artist, 'itemList': itemList, 'itemTypeList': itemTypeList}
	return render(request, 'ratings/viewArtist.html', context)