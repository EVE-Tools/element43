from django.contrib import admin

from apps.market_data.models import UUDIFMessage

class UUDIFMessageAdmin(admin.ModelAdmin):
    """
    Admin site definition for the UUDIFMessage model.
    """

    list_display = (
        'key', 'received_dtime', 'is_order',
    )
    list_filter = ('is_order', 'received_dtime')
    search_fields = ('key',)
    date_hierarchy = 'received_dtime'

admin.site.register(UUDIFMessage, UUDIFMessageAdmin)