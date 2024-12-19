from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    
    path("view_item/<str:id>", views.view_item, name="view_item"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<str:id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<str:id>", views.remove_watchlist, name="remove_watchlist"),
    path("categories", views.categories, name="categories"),
    path("view_category/<str:category>", views.view_category, name="view_category"),
    path("close_auction/<str:id>", views.close_auction, name="close_auction"),
    path("comment/<str:id>", views.comment, name="comment")
]
