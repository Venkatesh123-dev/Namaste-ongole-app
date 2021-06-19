from django.contrib import admin
from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin
from django.db.models import Count
from django.utils.safestring import mark_safe
from .models import Category, Product, Offer

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ("category", 'is_enabled', 'products_count')
    search_fields = ('category',)
    list_per_page = 25

    readonly_fields = ["category_image"]


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            products_count=Count("product", distinct=True),
        )
        return queryset

    def products_count(self, obj):
        return obj.products_count

    products_count.admin_order_field = 'products_count'

    def category_image(self, obj):
        return mark_safe('<img style="max-width: 240px;" src="{url}" />'.format(url = obj.image.url)
    )



    


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ("product", "price", "category", "slug", "is_enabled")
    search_fields = ('product',)
    list_filter = ("is_enabled", "category", )
    list_per_page = 25


    # list_display = ("product", "price", "category", "slug", "is_enabled")
    # search_fields = ('product',)
    # list_filter = ("is_enabled", "category", )
    # list_per_page = 25

# admin.site.register(CategoryAdmin)
# admin.site.register(Product)


@admin.register(Offer)
class OfferAdmin(ImportExportModelAdmin):
    # list_display = ("product", "price", "category", "slug", "is_enabled")
    # search_fields = ('product',)
    # list_filter = ("is_enabled", "category", )
    # list_per_page = 25

    readonly_fields = ["offer_image"]

    def offer_image(self, obj):
        return mark_safe('<img style="max-width: 240px;" src="{url}" />'.format(url = obj.image.url)
    )

admin.site.unregister(Group)
