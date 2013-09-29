from django.utils import simplejson
from django.core import serializers
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
import logging
import re

from models import Rating, Artist

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
	itemId = re.findall(r'rating-([^E]+)', unserializedData['item_id'])[0]
	ratingValue = int(unserializedData['value'])
	user = request.user

	logger.debug('Rating item id [%s] value [%d] for user [%s]' % (itemId, ratingValue, user.username))

	# Update the rating if it exists, otherwise create it
	try:
		rating = Rating.objects.get( user=user, item=itemId )
		rating.value = ratingValue
	except (Rating.DoesNotExist):
		rating = Rating( user=user, item=itemId, value=ratingValue )

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