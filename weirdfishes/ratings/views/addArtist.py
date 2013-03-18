from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from ratings.models import Artist

@login_required
def addArtist(request):
	artistName = request.POST['artist_name']

	artist = Artist(name=artistName)
	artist.save()
	artistId = artist.pk
	
	return HttpResponseRedirect(reverse('ratings:viewArtist', args=(artistId, )))