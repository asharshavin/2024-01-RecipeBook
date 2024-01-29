from django.contrib import admin

# Register your models here.
from .models import Dish, Product, Composition


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_editable  = ( 'title', )
    list_display_links = ('id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'quantity')
    list_editable  = ( 'title',  'quantity')
    list_display_links = ('id',)


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'dish', 'product', 'volume')
    list_editable = ('dish', 'product', 'volume')
    list_display_links = ('id',)
