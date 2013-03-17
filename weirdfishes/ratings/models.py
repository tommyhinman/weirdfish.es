from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import datetime

class Artist(models.Model):
	name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name

class Item(models.Model):
	ITEM_TYPES = (
		('A', 'Album'),
		('M', 'Movie'),
		('B', 'Book'),
	)
	artist = models.ForeignKey(Artist)
	name = models.CharField(max_length=255)
	item_type = models.CharField(max_length=2, choices=ITEM_TYPES)

	def __unicode__(self):
		return self.name

# class User(models.Model):
# 	name = models.CharField(max_length=255)
# 	nickname = models.CharField(max_length=255)

# 	def __unicode__(self):
# 		return self.name

class Rating(models.Model):
	user = models.ForeignKey(User)
	item = models.ForeignKey(Item)
	value = models.IntegerField()
	created_datetime = models.DateTimeField(default=datetime.datetime.now())

	def __unicode__(self):
		return 'Rating: {0}'.format(self.value)