import logging
import datetime
from string import split

from ratings.models import Artist, Item, Rating

logger = logging.getLogger('weirdfishes.ratings')

def processDataLine(itemData, formatInfo, user):

  #TODO: This code is super fragile right now, and desparately needs error checking and testing!

  itemData = split(itemData,'\t')
  logger.debug("line data: %s" % itemData)

  artistName = itemData[formatInfo["artistPos"]]
  albumName = itemData[formatInfo["albumPos"]]
  releaseDate = formatReleaseDate(itemData[formatInfo["releaseDatePos"]])
  rating = itemData[formatInfo["ratingPos"]]

  logger.debug("artist: %s, album: %s, rdate: %s, rating: %s" % (artistName, albumName, releaseDate, rating))

  if artistName != '' and albumName != '' and releaseDate != '':
    artist = addArtist(artistName)
    item = addAlbum(artist, albumName, releaseDate)

    if rating == '':
      rateItem(item, user, 0)
    else:
      rateItem(item, user, rating)
    
def formatReleaseDate(releaseDateStr):
  try:
    releaseDate = datetime.datetime.strptime(releaseDateStr, '%m/%d/%Y')
    logger.debug(releaseDate)
    return datetime.datetime.strftime(releaseDate, '%Y-%m-%d')
  except:
    return ''

def addArtist(artistName):
  try:
    artist = Artist.objects.get(name=artistName)
  except: 
    logger.debug("Creating new artist. Name: [%s]" % artistName)
    artist = Artist(name=artistName)

  artist.save()
  return artist

def addAlbum(artist, albumName, releaseDate):
  try:
    item = Item.objects.get(artist=artist, name=albumName)
  except:
    logger.debug("Creating new item. Artist: [%s] Item Name: [%s]" % (artist.name, albumName))
    item = Item(artist=artist, name=albumName, release_date=releaseDate, item_type='A')
    item.save()

  return item

def rateItem(item, user, value):
  # logger.debug("Adding rating: item [%s], user [%s], value [%s]" % (item, user, value))
  try:
    rating = Rating.objects.get(user=user, item=item)
    rating.value = value
  except (Rating.DoesNotExist):
    rating = Rating(user=user, item=item, value=value)

  rating.save()