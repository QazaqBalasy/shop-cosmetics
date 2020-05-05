from django.contrib import admin
from core.models import Cosmetic,CosmeticCategory,Basket,Order,UserFav , BankCard
# Register your models here.


class UserFavAdmin(admin.ModelAdmin):
    list_display = ['user', 'cosmetics', 'add_time']
    list_filter = ['user', 'cosmetics', 'add_time']
    search_fields = ['user', 'cosmetics']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['profile','date_added','confirmation_date']
    list_filter = ['profile','date_added','confirmation_date']
    search_fields = ['profile']


class BasketAdmin(admin.ModelAdmin):
    list_display = ['order','price']
    list_filter = ['order','price']


admin.site.register(Cosmetic)
admin.site.register(CosmeticCategory)
admin.site.register(Basket,BasketAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(UserFav,UserFavAdmin)
admin.site.register(BankCard)
