from django.contrib import admin
from core.models import Cosmetic,CosmeticCategory,Basket,Order,UserFav , BankCard
# Register your models here.


class UserFavAdmin(admin.ModelAdmin):
    list_display = ['user', 'cosmetics', 'add_time']
    list_filter = ['user', 'cosmetics', 'add_time']
    search_fields = ['user', 'cosmetics']

admin.site.register(Cosmetic)
admin.site.register(CosmeticCategory)
admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(UserFav,UserFavAdmin)
admin.site.register(BankCard)
