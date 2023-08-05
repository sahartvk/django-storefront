from django.contrib import admin
from . import models
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

# Register your models here.


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'collection_name']
    list_editable = ['unit_price']
    list_per_page = 10
    ordering = ['title']
    list_select_related = ['collection']
    list_filter = ['collection']
    actions = ['clear_inventory']
    # exclude = ['slug']
    prepopulated_fields = {
        'slug' : ['title']
    }
    autocomplete_fields = ['collection']
    search_fields = ['title']

    def collection_name(self, product):
        return product.collection.title

    @admin.action(description='clear inventory')
    def clear_inventory(self, request, queryset):
        count = queryset.update(inventory=0)
        self.message_user(request,
                          f'{count} messages were updated')
# admin.site.register(models.Product,ProductAdmin)

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    # extra = 0
    # min_num = 1
    # max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'payment_status']
    list_editable = ['payment_status']
    list_select_related = ['customer']
    inlines = [OrderItemInline]

    def customer_name(self, order):
        return order.customer.first_name

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({'collection__id': str(collection.id)}))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        # return format_html('<a href="http://google.com">{}</a>', collection.products_count)
        # return collection.products_count


    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )