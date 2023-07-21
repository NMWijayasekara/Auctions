from django.contrib import admin

from .models import User, Auction, Bid, Watchlist, Comment
# Register your models here.
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.site_title = "Auctions"
admin.site.site_header = "Auctions"