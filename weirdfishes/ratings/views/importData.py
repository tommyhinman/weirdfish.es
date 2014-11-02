from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

import logging

from ratings.utils import *

from ratings.models import Artist, Item, Rating

logger = logging.getLogger('weirdfishes.ratings')

@login_required
def importData(request):
  user = request.user
  data = request.POST['data']
  dataFormat = request.POST['dataFormat']

  dataFormat = split(dataFormat, ' ')
  artistPos = -1
  albumPos = -1
  releaseDatePos = -1
  ratingPos = -1

  formatInfo = {}

  for i in range(len(dataFormat)):
    formatVal = dataFormat[i].lower()
    if formatVal == "artist":
      formatInfo["artistPos"] = i
    if formatVal == "album":
      formatInfo["albumPos"] = i
    if formatVal == "releasedate":
      formatInfo["releaseDatePos"] = i
    if formatVal == "rating":
      formatInfo["ratingPos"] = i

  # logger.debug("artist: %d, album: %d, rdate: %d, rating: %d" % (artistPos, albumPos, releaseDatePos, ratingPos))

  importedDataList = []
  for line in data.splitlines():
    importedDataList.append(processDataLine(line, formatInfo, user))


  context = {'importedDataList': importedDataList}

  return render(request, 'ratings/importData.html', context)










