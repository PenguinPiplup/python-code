from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>/", views.wiki_find, name="wiki_find"),
    path("search/", views.search, name="search"),
    path("random/", views.random, name="random"),
    path("newpage/", views.newpage, name="newpage"),
    path("editpage/<str:TITLE>/", views.editpage, name="editpage")
]
