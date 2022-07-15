from django.urls import path
from . import views
from django.contrib import admin 
from django.conf import settings 
from django.conf.urls.static import static 


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<listing_id>", views.listing_page, name="listing_page"),
    path("watchlist/create/<listing_id>", views.create_watchlist, name="create_watchlist"),
    path("watchlist/remove/<listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist", views.view_watchlist, name="view_watchlist"),
    path("categories", views.categories_list, name="categories"),
    path("categories/<category>", views.category, name="category"),
    path("close/<listing_id>", views.close_listing, name="close_listing")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
