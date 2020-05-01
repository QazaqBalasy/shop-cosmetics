from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import CosmeticCategory, Cosmetic ,Order, Basket ,FavoriteCosmetic


class EditProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
             "pk",
             "username",
             "first_name",
             "last_name",
             "email",
             "date_joined",
         ]
        read_only_fields = ["pk","username", "date_joined","email"]


class CosmeticCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CosmeticCategory
        fields = ["url", "pk", "name", "description"]


class CosmeticSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=CosmeticCategory.objects.all(), slug_field="name"
    )
    class Meta:
        model = Cosmetic
        #read_only_fields = ["date_added", "date_updated"]
        fields = [
            "url",
            "pk",
            "name",
            "category",
            "price",
            "description",
            "color",
            "volume",
            "skin_type",
        ]
class BasketSerializer(serializers.ModelSerializer):
    cosmetic_id = serializers.IntegerField(source="cosmetic.pk", read_only=True)
    cosmetic = serializers.SlugRelatedField(slug_field="name", read_only=True)
    subtotal = serializers.DecimalField(decimal_places=2, max_digits=9, read_only=True)

    class Meta:
        model = Basket
        fields = ["cosmetic", "cosmetic_id", "quantity", "price", "subtotal"]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    products = BasketSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        decimal_places=2, max_digits=9, read_only=True
    )

    class Meta:
        model = Order
        read_only_fields = ["date_added", "date_updated", "confirmation_date"]
        fields = [
            "url",
            "pk",
            "date_added",
            "date_updated",
            "confirmation_date",
            "street",
            "street_number",
            "flat_number",
            "zip_code",
            "city",
            "province",
            "total_price",
            "products",
        ]


class FavoriteCosmeticSerializer(serializers.HyperlinkedModelSerializer):
    cosmetic_id = serializers.IntegerField(source="cosmetic.pk", read_only=True)
    cosmetic_name = serializers.SlugRelatedField(slug_field="name", read_only=True)
    cosmetic_price = serializers.SlugRelatedField(slug_field="price", read_only=True)
    cosmetic_category = serializers.SlugRelatedField(slug_field="category", read_only=True)



    class Meta:
        model = FavoriteCosmetic
        fields = [
            #"url",
            "pk",
            "cosmetic_id",
            "cosmetic_name",
            "cosmetic_price",
            "cosmetic_category",

        ]
