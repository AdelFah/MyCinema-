
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),

    path("category/<str:category>/", views.catalog, name="category_catalog"),

    path("add/", views.item_create, name="item_create"),
    path("watchlist/", views.watchlist, name="watchlist"),

    path("<int:pk>/", views.item_detail, name="item_detail"),
    path("<int:pk>/edit/", views.item_edit, name="item_edit"),

    path("<int:pk>/status/", views.update_item_status, name="update_item_status"),
    path("<int:pk>/watchlist/", views.toggle_watchlist, name="toggle_watchlist"),
]

