from django.contrib import admin
from core.models import Cosmetic,CosmeticCategory,Basket,Order,FavoriteCosmetic
# Register your models here.
admin.site.register(Cosmetic)
admin.site.register(CosmeticCategory)
admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(FavoriteCosmetic)
