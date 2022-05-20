from django.contrib import admin
from productapp.models import Product,Contact,LineItem,Order,CartItem
# Register your models here.

admin.site.site_header = "Product Buying page"
admin.site.site_title = "Admin Page"
admin.site.index_title = "Admin Page of Products and Users"

class ProductList(admin.ModelAdmin):
    list_display = ('name','price','desc','seller_name',)
    search_fields = ('name','desc','price',)

    def set_price_to_zero(self,request,queryset):
        queryset.update(price=0)

    def change_seller_name(self,request,queryset):
        queryset.update(seller_name=2)

    actions = ('set_price_to_zero','change_seller_name',)
    list_editable = ('price','desc',)


admin.site.register(Product,ProductList)
admin.site.register(LineItem)
admin.site.register(CartItem)

class ContactList(admin.ModelAdmin):
    list_display = ('name','email','phone')

admin.site.register(Contact,ContactList)

class OrderList(admin.ModelAdmin):
    list_display = ('name','email','date','paid')
    list_editable = ('paid',)

admin.site.register(Order,OrderList)