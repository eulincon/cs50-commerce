from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.addRemoveWatchlist, name="addRemoveWatchlist"),
    path("bid", views.bid, name="bid"),
    path("close_auction/<int:auction_id>", views.closeAuction, name="close_auction"),
    path("handle_comment/<int:auction_id>", views.handle_comment, name="handle_comment")
]
