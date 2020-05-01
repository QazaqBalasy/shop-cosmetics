from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth import logout, get_user_model
# from django_filters import rest_framework as filters
# from django_filters import AllValuesFilter, NumberFilter, DateTimeFilter
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import User, CosmeticCategory,Cosmetic,Basket ,Order , FavoriteCosmetic
from .serializers import (
                    EditProfileUserSerializer,
                    CosmeticSerializer,
                    CosmeticCategorySerializer ,
                    BasketSerializer,
                    OrderSerializer,
                    FavoriteCosmeticSerializer,)

from .permissions import IsAdminUserOrReadOnly

class MyProfile(generics.RetrieveUpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = EditProfileUserSerializer
    name = "userprofile-me"
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    # model = get_user_model()


    def get_object(self, queryset=None):
        return self.request.user
    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = generics.get_object_or_404(queryset=queryset, user=self.request.user)
    #     return obj


class CosmeticCategoryList(generics.ListCreateAPIView):
    queryset = CosmeticCategory.objects.all()
    serializer_class = CosmeticCategorySerializer
    name = "cosmeticcategory-list"
    filter_fields = ["name"]
    search_fields = ["^name"]
    ordering_fields = ["name"]
    #permission_classes = [IsAdminUserOrReadOnly]


class CosmeticCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CosmeticCategory.objects.all()
    serializer_class = CosmeticCategorySerializer
    name = "cosmeticcategory-detail"
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdminUserOrReadOnly]


class CosmeticList(generics.ListCreateAPIView):
    queryset = Cosmetic.objects.all()
    serializer_class = CosmeticSerializer
    name = "cosmetic-list"
    #filter_class = ProductFilter
    ordering_fields = ["name", "price"]
    search_fields = ["^name"]
    #permission_classes = [IsAdminUserOrReadOnly]


class CosmeticDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cosmetic.objects.all()
    serializer_class = CosmeticSerializer
    name = "cosmetic-detail"
    #permission_classes = [IsAdminUserOrReadOnly]


class AddProduct(generics.CreateAPIView):
    serializer_class = BasketSerializer
    name = "cosmetic-add"
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = Order.objects.get(
            profile=self.request.user, confirmation_date__isnull=True
        )
        cosmetic = get_object_or_404(Cosmetic, pk=self.kwargs["pk"])
        serializer.save(cosmetic_id=cosmetic.id, order_id=order.id, price=cosmetic.price)

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except ObjectDoesNotExist:
            data = {"detail": "You have to create new order first."}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            data = {"detail": "You cannot duplicate the product in the same order."}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class BasketProductList(generics.ListAPIView):
    serializer_class = BasketSerializer
    name = "basket-list"
    #filter_class = BasketFilter
    ordering_fields = ["cosmetic", "quantity", "price"]
    search_fields = ["^cosmetic__name"]
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Basket.objects.filter(
            order__profile=self.request.user, order=self.kwargs["order_pk"]
        )#
        return queryset


# TODO: Test BasketProductDetail view
class BasketProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BasketSerializer
    name = "basket-detail"
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Basket.objects.filter(
            order__profile=self.request.user, order=self.kwargs["order_pk"]
        )
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(
            queryset=queryset, cosmetic=self.kwargs["cosmetic_pk"]
        )
        return obj

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.order.confirmation_date is not None:
            data = {"detail": "You cannot remove a product from a closed order."}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.order.is_locked():
            data = {"detail": "You cannot modify an item from a closed order."}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().update(request, *args, **kwargs)


class UpdateUnconfirmedOrderMixin(object):
    def update_unconfirmed_order(self, confirm=False):
        try:
            order = Order.objects.get(
                confirmation_date__isnull=True, profile=self.request.user
            )
        except ObjectDoesNotExist:
            return
        order.update_data(confirm)


# TODO: Test OrderList view
class OrderList(UpdateUnconfirmedOrderMixin, generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    name = "order-list"
    #filter_class = OrderFilter
    ordering_fields = ["date_updated", "date_added", "confirmation_date"]
    #search_fields = ["^street"]
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.filter(profile=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)

    def post(self, request, *args, **kwargs):
        unconfirmed_order = Order.objects.filter(
            confirmation_date__isnull=True, profile=self.request.user
        ).count()
        if unconfirmed_order == 0:
            return super().post(request, *args, **kwargs)
        elif unconfirmed_order == 1:
            data = {"detail": "You can have only one active order."}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {"detail": "Internal error occurred, please contact administrator"}
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        self.update_unconfirmed_order()
        return super().get(request, *args, **kwargs)


class OrderDetail(generics.RetrieveDestroyAPIView):
    serializer_class = OrderSerializer
    name = "order-detail"
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.filter(profile=self.request.user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_locked():
            instance.update_data()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        if not order.is_locked():
            return super().delete(request, *args, **kwargs)
        else:
            data = {"detail": "You cannot delete a confirmed order."}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


# TODO: Test ConfirmOrder view
class ConfirmOrder(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    name = "order-confirm"
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.filter(profile=self.request.user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_locked():
            instance.update_data(confirm=True)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ConfirmedOrderList(generics.ListAPIView):
    queryset = Order.objects.filter(confirmation_date__isnull=False)
    serializer_class = OrderSerializer
    name = "confirmedorder-list"
    #filter_class = OrderFilter
    ordering_fields = ["confirmation_date", "date_updated", "date_added"]
    ordering = ["-confirmation_date"]
    #search_fields = ["^street"]
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]


# TODO: Test ConfirmedOrderDetail view
class ConfirmedOrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.filter(confirmation_date__isnull=False)
    serializer_class = OrderSerializer
    name = "confirmedorder-detail"
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]


class FavoriteCosmeticList(generics.ListCreateAPIView):
    serializer_class = FavoriteCosmeticSerializer
    name = "favorite-cosmetics"
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = FavoriteCosmetic.objects.filter(
            profile=self.request.user
        )#
        return queryset

    def perform_create(self, serializer):
        cosmetic = get_object_or_404(Cosmetic, pk=self.kwargs["pk"])
        profile = profile=self.request.user
        serializer.save(cosmetic_id=cosmetic.id,profile_id=profile.pk)




class FavoriteCosmeticDelete(generics.DestroyAPIView):
    serializer_class = FavoriteCosmeticSerializer
    name = "favorite-cosmetics"
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = FavoriteCosmetic.objects.filter(
            profile=self.request.user
        )#
        return queryset
