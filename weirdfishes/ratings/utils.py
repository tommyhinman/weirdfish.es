import logging
import datetime
from string import split

from ratings.models import Artist, Item, Rating

logger = logging.getLogger('weirdfishes.ratings')

#TODO: Namespace conflicts are causing problems here. I've renamed
#The functions for now, but this needs to be better encapsulated

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
    artist = addArtistToDb(artistName)
    item = addAlbumToDb(artist, albumName, releaseDate)

    if rating == '':
      rateItemInDb(item, user, 0)
      return "Artist: %s, Album: %s, Release Date: %s, Rating %s" % (artistName, albumName, releaseDate, 0)
    else:
      rateItemInDb(item, user, rating)
      return "Artist: %s, Album: %s, Release Date: %s, Rating %s" % (artistName, albumName, releaseDate, rating)
    
def formatReleaseDate(releaseDateStr):
  try:
    releaseDate = datetime.datetime.strptime(releaseDateStr, '%m/%d/%Y')
    logger.debug(releaseDate)
    return datetime.datetime.strftime(releaseDate, '%Y-%m-%d')
  except:
    return ''

def addArtistToDb(artistName):
  try:
    artist = Artist.objects.get(name=artistName)
  except: 
    logger.debug("Creating new artist. Name: [%s]" % artistName)
    artist = Artist(name=artistName)

  artist.save()
  return artist

def addAlbumToDb(artist, albumName, releaseDate):
  try:
    item = Item.objects.get(artist=artist, name=albumName)
  except:
    logger.debug("Creating new item. Artist: [%s] Item Name: [%s]" % (artist.name, albumName))
    item = Item(artist=artist, name=albumName, release_date=releaseDate, item_type='A')
    item.save()

  return item

def rateItemInDb(item, user, value):
  # logger.debug("Adding rating: item [%s], user [%s], value [%s]" % (item, user, value))
  try:
    rating = Rating.objects.get(user=user, item=item)
    rating.value = value
  except (Rating.DoesNotExist):
    rating = Rating(user=user, item=item, value=value)

  rating.save()