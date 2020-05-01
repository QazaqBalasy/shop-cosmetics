from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [
    path("me/", views.MyProfile.as_view(), name=views.MyProfile.name),
    path(
        "cosmetic-categories/",
        views.CosmeticCategoryList.as_view(),
        name=views.CosmeticCategoryList.name,
    ),
    path(
        "cosmetic-categories/<int:pk>/",
        views.CosmeticCategoryDetail.as_view(),
        name=views.CosmeticCategoryDetail.name,
    ),
    path("cosmetics/", views.CosmeticList.as_view(), name=views.CosmeticList.name),
    path(
        "cosmetics/<int:pk>/",
        views.CosmeticDetail.as_view(),
        name=views.CosmeticDetail.name,
    ),
    path(
        "cosmetics/<int:pk>/add/", views.AddProduct.as_view(), name=views.AddProduct.name
    ),
    path(
        "orders/<int:order_pk>/cosmetics/",
        views.BasketProductList.as_view(),
        name=views.BasketProductList.name,
    ),
    path(
        "orders/<int:order_pk>/cosmetics/<int:cosmetic_pk>/",
        views.BasketProductDetail.as_view(),
        name=views.BasketProductDetail.name,
    ),
    path("orders/", views.OrderList.as_view(), name=views.OrderList.name),
    path("orders/<int:pk>/", views.OrderDetail.as_view(), name=views.OrderDetail.name),
    path(
        "orders/<int:pk>/confirm/",
        views.ConfirmOrder.as_view(),
        name=views.ConfirmOrder.name,
    ),
    path(
        "confirmed-orders/",
        views.ConfirmedOrderList.as_view(),
        name=views.ConfirmedOrderList.name,
    ),
    path(
        "confirmed-orders/<int:pk>/",
        views.ConfirmedOrderDetail.as_view(),
        name=views.ConfirmedOrderDetail.name,
    ),
    path(
        "cosmetics/<int:pk>/add-favorite/", views.FavoriteCosmeticList.as_view(),name=views.FavoriteCosmeticList.name
    ),
    path(
        "favorites/", views.FavoriteCosmeticList.as_view(),name=views.FavoriteCosmeticList.name
    ),
    path(
        "favorites/<int:cosmetic_pk>/", views.FavoriteCosmeticDelete.as_view(),name=views.FavoriteCosmeticDelete.name
    ),
]
