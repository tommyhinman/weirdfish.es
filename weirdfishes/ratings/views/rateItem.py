from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from ratings.models import Artist, Item, Rating

@login_required
def rateItem(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	value = request.POST['value']
	user = request.user

	# Update the rating if it exists, otherwise create it
	try:
		rating = Rating.objects.get( user=user, item=item )
		rating.value = value
	except (Rating.DoesNotExist):
		rating = Rating( user=user, item=item, value=value )

	rating.save()

	return HttpResponseRedirect(reverse('ratings:viewItem', args=(item.id, )))