from django.contrib import admin

# Register your models here.
from mainapp.models import ProductCategories, Products

admin.site.register(ProductCategories)

@admin.register(Products)
class Products(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'image', 'description', ('price', 'quantity'), 'category')
    readonly_fields = ('category', )
    ordering = ('name', 'price')
    search_fields = ('name', )