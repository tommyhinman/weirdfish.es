from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
import logging
import re

from models import Rating

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