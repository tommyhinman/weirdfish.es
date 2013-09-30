from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from ratings.models import User

@login_required
def viewAllUsers(request):
	userList = User.objects.all().annotate(rating_count=Count('rating'))
	context = {'userList': userList,}
	return render(request, 'ratings/viewAllUsers.html', context)