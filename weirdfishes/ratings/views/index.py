from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ratings.models import Artist, Item, Rating

@login_required
def index(request):
	#if not request.user.is_authenticated():
	#	return redirect('/google/login/?next=%s' % request.path)

	artistList = Artist.objects.all()
	user = request.user
	context = {'artistList' : artistList, 'user': user}
	return render(request, 'ratings/index.html', context)