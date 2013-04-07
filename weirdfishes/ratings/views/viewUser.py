from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime

from ratings.models import Artist, Item, Rating, User


@login_required
def viewUser(request, user_id):
	userToView = get_object_or_404(User, pk=user_id)
	yearFilter = request.GET.get('yearFilter') or 0
	ratingList = Rating.objects.filter(user=user_id)
	if( yearFilter ):
		try:
			yearFilter = int(yearFilter)
			if(yearFilter > 1000 and yearFilter < 3000):
				dateRangeStart = datetime(yearFilter, 1, 1)
				dateRangeEnd = datetime(yearFilter, 12, 31)
				ratingList = ratingList.filter(item__release_date__gte=dateRangeStart).filter( item__release_date__lte=dateRangeEnd)
		except ValueError:
			#invalid year input
			yearFilter = 0

	context = {'userToView': userToView, 'ratingList': ratingList, 'yearFilter': yearFilter}
	return render(request, 'ratings/viewUser.html', context)