from django.utils import simplejson
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

import logging
import re
from datetime import date, timedelta, datetime

from models import Rating, Artist, Item, User

logger = logging.getLogger('weirdfishes.ratings')

@dajaxice_register
def say_hello(request):
	dajax = Dajax()
	dajax.alert("Hello world!")
	return dajax.json()

@dajaxice_register
def rate_item(request, data):

	dajax = Dajax()
	unserializedData = simplejson.loads(data)
	itemId = int(unserializedData['item_id'])
	ratingValue = int(unserializedData['value'])
	user = request.user

	logger.debug('Rating item id [%s] value [%d] for user [%s]' % (itemId, ratingValue, user.username))

	ratedDate = datetime.today()
	# Update the rating if it exists, otherwise create it
	try:
		rating = Rating.objects.get( user=user, item=itemId )
		rating.value = ratingValue
		rating.created_datetime = ratedDate
	except (Rating.DoesNotExist):
		item = Item.objects.get(id=itemId)
		rating = Rating( user=user, item=item, value=ratingValue, created_datetime=ratedDate )

	rating.save()

	return dajax.json()

@dajaxice_register
def get_artist_list(request, data):
	dajax = Dajax()
	data = simplejson.loads(data)
	nameStartsWith = data['name_starts_with']
	
	maxRows = data['max_rows']
	try:
		maxRows = int(maxRows)
		if(maxRows > 25):
			maxRows = 25
	except ValueError:
		maxRows = 10

	logger.debug('Getting [%d]artists that start with [%s] ' % (maxRows, nameStartsWith))

	artistList = Artist.objects.filter(name__istartswith=nameStartsWith)[:maxRows]
	serializedArtistList = serializers.serialize('json', artistList)
	logger.debug(serializedArtistList)
	return serializedArtistList

@dajaxice_register
def render_rating_list(request, user_id, year_filter, viewUnrated, viewRecentlyRated):
	dajax = Dajax()

	userToView = get_object_or_404(User, pk=user_id)
	ratingList = Rating.objects.filter(user=user_id)

	if(viewUnrated):
		ratingList = ratingList.filter(value=0)

	if(viewRecentlyRated):
		today = datetime.today()
		dateRangeStart = today - timedelta(days=14)
		ratingList = ratingList.filter(created_datetime__gte=dateRangeStart)
		ratingList = ratingList.order_by('created_datetime').reverse()

	if(year_filter):
		try:
			year_filter = int(year_filter)
			if(year_filter > 1000 and year_filter < 3000):
				dateRangeStart = datetime(year_filter, 1, 1)
				dateRangeEnd = datetime(year_filter, 12, 31)
				ratingList = ratingList.filter(item__release_date__gte=dateRangeStart).filter(item__release_date__lte=dateRangeEnd)
		except ValueError:
			#invalid year input
			year_filter = 0

	context = {'userToView': userToView, 'ratingList': ratingList}
	render = render_to_string('ratings/ratingList.html', context)
	dajax.assign('#ratingList', 'innerHTML', render)

	return dajax.json()