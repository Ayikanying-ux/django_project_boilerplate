from django.urls import path
from .views import HomeView, checkout_page, ItemDetailView, add_to_cart, remove_from_cart

app_name = 'core'
urlpatterns = [
    path("", HomeView.as_view(), name="item-list"),
    path("product/<slug>/", ItemDetailView.as_view(), name="product-page"),
    path("checkout", checkout_page, name="checkout-page"),
    path("add-to-cart/<slug>/", add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<slug>/", remove_from_cart, name="remove_from_cart"),
]
