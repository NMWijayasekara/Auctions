from django.urls import path

from . import views

urlpatterns = [
    path("", views.active_listings, name="active_listings"),
    path("allauctions/", views.index, name="index"),
    path("close/<str:title>/", views.close_auction, name="close_auction"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<str:title>", views.auction, name="auction"),
    path("new/", views.new, name="new"),
    path("myauctions/", views.my_auctions, name="myauctions"),
    path("auction/watch/<str:title>", views.watchlist, name="watchlist"),
    path("mywatchlists/", views.my_watchlists, name="mywatchlists"),
    path("catelogs/", views.catelogs, name="catelogs"),
    path("catelogs/<str:catelog>", views.view_catelog, name="view_catelog")
]
