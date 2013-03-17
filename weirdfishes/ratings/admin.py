from django.contrib import admin
from ratings.models import Artist, Item, User, Rating

admin.site.register(Artist)
admin.site.register(Item)
#admin.site.register(User)
admin.site.register(Rating)