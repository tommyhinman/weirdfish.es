from django.utils import simplejson
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

import logging
import re
import uuid
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
	ratingList = Rating.objects.select_related().filter(user=user_id)

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

@dajaxice_register
def add_artists(request, data):
	dajax = Dajax()
	data = simplejson.loads(data)
	count = int(data['count'])

	for i in range(count):
		artistName = ("test_artist_%d") % (uuid.uuid4())
		artist = Artist(name=artistName)
		artist.save()

	successMessage = "Successfully added [%d] artists!" % count
	dajax.assign('#message', 'innerHTML', successMessage)

	return dajax.json()

@dajaxice_register
def add_items(request, data):
	dajax = Dajax()
	data = simplejson.loads(data)
	count = int(data['count'])
	artist_name = data['artist_name']

	artist = get_object_or_404(Artist, name=artist_name)


	for i in range(count):
		itemName = ("test_item_%d") % (uuid.uuid4())
		logger.debug("Making item with name [%s]" % itemName)

		item = Item( artist=artist, name=itemName, release_date="1989-11-11", item_type='A')
		item.save()

	successMessage = "Successfully added [%d] items to artist [%s]" % (count, artist_name)
	dajax.assign('#message', 'innerHTML', successMessage)

	return dajax.json()

@dajaxice_register
def clear_test_data(request, data):
	dajax = Dajax()

	Item.objects.filter(name__icontains="test_item").delete()
	Artist.objects.filter(name__icontains="test_artist").delete()

	successMessage = "Successfully deleted all test data."
	dajax.assign('#message', 'innerHTML', successMessage)
	return dajax.json()


