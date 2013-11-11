from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ratings.models import Artist

@login_required
def tools(request):
	# user = request.user

	context = {}

	return render(request, 'ratings/tools.html', context)

