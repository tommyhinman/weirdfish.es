from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count
from ratings.models import Artist, Item, Rating

import logging

logger = logging.getLogger('weirdfishes.ratings')

# @login_required
def index(request):
	if not request.user.is_authenticated():
		return redirect('/login/?next=%s' % request.path)

	logger.debug('test3')

	artistList = Artist.objects.all().annotate(item_count=Count('item'))
	# for artist in artistList:
	# 	artist.item_count = Item.objects.filter(artist=artist).aggregate(Sum('item'))['item__sum']

	user = request.user
	context = {'artistList' : artistList, 'user': user}
	return render(request, 'ratings/index.html', context)