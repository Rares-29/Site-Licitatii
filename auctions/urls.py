from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("product/<str:product_id>", views.product, name = "product"),
    path("category/<str:category>", views.category, name = "category"),
    path("categories", views.category_general, name = "categories"),
    path("create_listing", views.create_listing, name = "create_listing"),
    path("watchlist", views.watchlist, name = "watchlist")
]
