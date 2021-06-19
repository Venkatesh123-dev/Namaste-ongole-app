from django.contrib import admin
from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin
from django.db.models import Count
from django.utils.safestring import mark_safe
from .notification_adapter import notificationManager
from .models import Order, Payment, OrderProduct, Address

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    list_display = ( "user", 'items', 'amount', 'ordered_on',
                    'order_placed', 'received', 'order_type',
                    'payment_status', 'gateway_order_id')
    list_filter = ("order_placed", 'order_type', 'payment_status',
                   "out_for_delivered", "received")

   # date_hierarchy = 'ordered_date'

    def get_readonly_fields(self, request, obj=None):
        non_editable_fields = [
            "products",
            'user',
            'shipping_address',
            "order_type",
            "payment_status",
            "gateway_order_id",
            "gateway_order_response",
            "coupon",
        ]
        if obj:
            if obj.received:
                non_editable_fields.insert(0, 'received')

            if obj.out_for_delivered:
                non_editable_fields.insert(0, 'out_for_delivered')

            if obj.order_placed:
                non_editable_fields.insert(0, 'order_placed')

            return non_editable_fields
        else:
            return []

    # list_per_page = 25

    # readonly_fields = ["category_image"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # queryset = queryset.annotate(
        #     products_count=Count("product", distinct=True),
        # )
        return queryset.filter(gateway_order_id__isnull=False)

    def items(self, obj):
        return obj.ordered_products_count

    def amount(self, obj):
        return obj.get_total

    def is_order(self, obj):
        return True if obj.order_placed else False

    def ordered_on(self, obj):
        return obj.ordered_date

    def delivered(self, obj):
        return obj.received

    def location(self, obj):
        return obj.shipping_address.full_address

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # obj.added_by = request.user
        notificationManager.send_order_updates(obj)
        super().save_model(request, obj, form, change)

    # products_count.admin_order_field = 'products_count'

    # def category_image(self, obj):
    #     return mark_safe('<img style="max-width: 240px;" src="{url}" />'.format(url = obj.image.url)
    # )


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    pass


@admin.register(OrderProduct)
class OrderProductAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Address)

# list_display = ("product", "price", "category", "slug", "is_enabled")
# list_filter = ("is_enabled", "category", )
# list_per_page = 25

# admin.site.register(CategoryAdmin)
# admin.site.register(Product)

# admin.site.unregister(Group)
