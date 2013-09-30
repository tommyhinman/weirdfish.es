from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from ratings.models import Artist, Item, Rating

@login_required
def deleteItem(request, item_id):
	user = request.user
	artist = Artist.objects.get(pk=request.POST['artist_id'])
	Item.objects.get(id=item_id).delete()

	return HttpResponseRedirect(reverse('ratings:viewArtist', args=(artist.id,)))