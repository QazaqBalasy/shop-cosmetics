from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator
from decimal import *
from django.utils import timezone
from datetime import datetime,time
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class CosmeticCategory(models.Model):
    """Categories for cosmetic products"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Cosmetic(models.Model):
    #Id = models.IntegerField(unique=True,primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    price = models.DecimalField(max_digits=9,decimal_places=3)
    brand = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    category = models.ForeignKey(
        CosmeticCategory, on_delete=models.CASCADE, related_name="cosmetics"
    )
    image_url = models.CharField(max_length=255,blank=True,null=True)
    description = models.CharField(max_length=255,blank=True,null=True)
    color = models.CharField(max_length=25,blank=True,null=True)
    skin_type = models.CharField(max_length=25,blank=True,null=True)
    volume = models.CharField(max_length=25,blank=True,null=True)
    target_area = models.CharField(max_length=25,blank=True,null=True)

    def __str__(self):
        return (self.name + " " + self.brand)


class Order(models.Model):
    """Order which user made"""
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    confirmation_date = models.DateTimeField(null=True, default=None, editable=False)
    profile = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", editable=False
    )
    street = models.CharField(max_length=255, blank=True)
    street_number = models.CharField(max_length=10, blank=True)
    flat_number = models.CharField(max_length=10, blank=True)
    zip_code = models.CharField(
        max_length=6,
        help_text="Valid zip code (000000)",
        blank=True,
    )
    city = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=12,blank=True)

    def is_locked(self):
        return self.confirmation_date is not None

    def total_price(self): #
        total = Decimal(0)
        for cosmetic in self.cosmetics.all():
            total += cosmetic.subtotal()

        return total

    def update_data(self, confirm=False):

        for cosmetic in self.cosmetics.all():
            cosmetic.update_price()

        if confirm:
            self.confirmation_date = timezone.now()

        # self.street = self.profile.street
        # self.street_number = self.profile.street_number
        # self.flat_number = self.profile.flat_number
        # self.zip_code = self.profile.zip_code
        # self.city = self.profile.city
        # self.province = self.profile.province

        #self.full_clean()
        self.save()


class Basket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="cosmetics")
    cosmetic = models.ForeignKey(
        Cosmetic, on_delete=models.CASCADE, related_name="baskets"
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(editable=False, decimal_places=3, max_digits=9)

    def is_locked(self):
        return self.order.confirmation_date is not None

    def update_price(self):
        if self.is_locked():
            raise Exception("You cannot confirm locked basket.")

        self.price = self.cosmetic.price

        self.full_clean()
        self.save()

    def subtotal(self):
        return self.price * Decimal(self.quantity)

    def __str__(self):
        return "{0}: {1} x{2}".format(self.order.pk, self.cosmetic.name, self.quantity)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["order", "cosmetic"], name="unique_cosmetics_order"
            )
        ]


class UserFav(models.Model):
    """
    Favorite Cosmetics of user
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    cosmetics = models.ForeignKey(Cosmetic, on_delete=models.CASCADE, verbose_name='favorites', help_text='selected')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='added date')

    class Meta:
        verbose_name = 'Favorites'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'cosmetics')

    def __str__(self):
        return self.user.username


class BankCard(models.Model):
    number = models.DecimalField(max_digits=16,decimal_places=0)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    CVC = models.DecimalField(max_digits=3,decimal_places=0)
    date = models.CharField( max_length=5,verbose_name='expiration date');
    user = models.ForeignKey(User,on_delete= models.CASCADE,related_name="card")

    class Meta:
        unique_together = (("user", "number"),)
