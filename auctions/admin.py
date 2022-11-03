from django.contrib import admin

from .models import User
from .models import Bid,Item,Comment,Category,Watchlist
# Register your models here.

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist)