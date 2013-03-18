from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from ratings.models import Artist, Item, Rating

@login_required
def viewItem(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	artist = item.artist
	ratingList = Rating.objects.filter(item=item)
	context = {'artist': artist, 'item': item, 'ratingList': ratingList}
	return render(request, 'ratings/viewItem.html', context)