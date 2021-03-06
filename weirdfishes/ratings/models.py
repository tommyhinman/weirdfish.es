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
	release_date = models.DateField()

	def __unicode__(self):
		return self.name

class Rating(models.Model):
	user = models.ForeignKey(User)
	item = models.ForeignKey(Item)
	value = models.IntegerField()
	notes = models.TextField(null=True)
	created_datetime = models.DateTimeField(default=datetime.datetime.now())

	def __unicode__(self):
		return 'Rating: {0}'.format(self.value)

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	nickname = models.CharField(max_length=100, blank=True, null=True)