from django.contrib import admin
from .models import Product, Category
from mptt.admin import MPTTModelAdmin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, MPTTModelAdmin)
