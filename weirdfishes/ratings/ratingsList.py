import logging
from datetime import date, timedelta, datetime

from models import Rating, Artist, Item, User

class RatingsList:
	"""This class represents a list of ratings"""

	def __init__(self, user):
		self.user = user

	def getFullRatingList(self, yearFilter, viewUnrated, viewRecentlyRated):
		ratingList = Rating.objects.select_related().filter(user=self.user)

		if(viewUnrated):
			ratingList = ratingList.filter(value=0)

		if(viewRecentlyRated):
			today = datetime.today()
			dateRangeStart = today - timedelta(days=14)
			ratingList = ratingList.filter(created_datetime__gte=dateRangeStart)
			ratingList = ratingList.order_by('created_datetime').reverse()

		if(yearFilter):
			try:
				yearFilter = int(yearFilter)
				if(yearFilter > 1000 and yearFilter < 3000):
					dateRangeStart = datetime(yearFilter, 1, 1)
					dateRangeEnd = datetime(yearFilter, 12, 31)
					ratingList = ratingList.filter(item__release_date__gte=dateRangeStart).filter(item__release_date__lte=dateRangeEnd)
			except ValueError:
				#invalid year input
				yearFilter = 0

		return ratingList

	def getListeningQueue(self, size):
		ratingList = Rating.objects.select_related().filter(user=self.user)

		# Only view unrated
		ratingList = ratingList.filter(value=0)
		
		# Only view for current year
		currentYear = date.today().year
		dateRangeStart = datetime(currentYear, 1, 1)
		dateRangeEnd = datetime(currentYear, 12, 31)
		ratingList = ratingList.filter(item__release_date__gte=dateRangeStart).filter(item__release_date__lte=dateRangeEnd)

		# Order by release date
		ratingList = ratingList.order_by('item__release_date')

		# Get only the first SIZE elements
		ratingList = ratingList[:size]

		return ratingList
