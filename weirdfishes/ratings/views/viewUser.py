from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from ratings.models import Artist, Item, Rating, User

@login_required
def viewUser(request, user_id):
	userToView = get_object_or_404(User, pk=user_id)
	ratingList = Rating.objects.filter(user=user_id)

	context = {'userToView': userToView, 'ratingList': ratingList}
	return render(request, 'ratings/viewUser.html', context)