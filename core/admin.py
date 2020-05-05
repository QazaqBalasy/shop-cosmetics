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

admin.site.register(Cosmetic)
admin.site.register(CosmeticCategory)
admin.site.register(Basket)
admin.site.register(Order,OrderAdmin)
admin.site.register(UserFav,UserFavAdmin)
admin.site.register(BankCard)
