from django.urls import path
from . import views

urlpatterns = [
    path("", views.marketplace, name="marketplace"),
    path("<slug:vendor_slug>/", views.vendor_detail, name="vendor_detail"),

    #ADD TO CART
    path("add-to-cart/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    #DECREASE CART ITEM QUANTITY
    path("decrease-cart/<int:item_id>/", views.decrease_cart, name="decrease_cart"),
    #delete cart item
    path("delete-cart/<int:item_id>/", views.delete_cart, name="delete_cart"),
]

  