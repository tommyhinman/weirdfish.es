from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ratings.models import User, Item, Artist

@login_required
def search(request):
	query = request.GET['q']
	userList = User.objects.filter(username__icontains=query)
	itemList = Item.objects.filter(name__icontains=query)
	artistList = Artist.objects.filter(name__icontains=query)
	activeTab = getActiveTab(userList, itemList, artistList)

	context = {'userList': userList, 'artistList':artistList, 'itemList': itemList, 'activeTab' : activeTab}
	return render(request, 'ratings/search.html', context)

def getActiveTab(userList, itemList, artistList):
	if(artistList):
		return "artist"
	elif(itemList):
		return "item"
	elif(userList):
		return "user"
	else:
		return ""
