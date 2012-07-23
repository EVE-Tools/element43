from django.contrib import admin
from apps.market_data.models import UUDIFMessage, Orders

class UUDIFMessageAdmin(admin.ModelAdmin):
    """
    Admin site definition for the UUDIFMessage model.
    """

    list_display = ('key', 'received_dtime', 'is_order')
    list_filter = ('is_order', 'received_dtime')
    search_fields = ('key',)
    date_hierarchy = 'received_dtime'

admin.site.register(UUDIFMessage, UUDIFMessageAdmin)

class OrdersAdmin(admin.ModelAdmin):
    """
    Admin site definition for the Orders model.
    """

    list_display = ('id', 'type_id', 'region_id', 'price', 'generated_at', 'is_bid')
    list_filter = ('is_bid', 'generated_at', 'type_id')
    search_fields = ('type_id', 'message_key', 'uploader_ip_hash')
    date_hierarchy = 'generated_at'

admin.site.register(Orders, OrdersAdmin)