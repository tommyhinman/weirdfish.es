from django.utils import simplejson
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

import logging
import re
import uuid
from ratingsList import RatingsList
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

	ratingsToDisplay = RatingsList(userToView).getFullRatingList(year_filter, viewUnrated, viewRecentlyRated)

	context = {'userToView': userToView, 'ratingList': ratingsToDisplay}
	render = render_to_string('ratings/ratingList.html', context)
	dajax.assign('#ratingList', 'innerHTML', render)

	return dajax.json()

@dajaxice_register
def render_listening_queue(request, user_id):
	dajax = Dajax()
	userToView = get_object_or_404(User, pk=user_id)
	ratingsToDisplay = RatingsList(userToView).getListeningQueue(10)

	context = {'userToView': userToView, 'ratingList': ratingsToDisplay}
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


