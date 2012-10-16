"""
Model definitions for storing market data messages.
"""

from django.db import models

#
# Market Data Models
#


class UUDIFMessage(models.Model):
    """
    A raw JSON UUDIF market message. This is typically only used on local
    development workstations.
    """
    key = models.CharField(max_length=255, unique=True,
        help_text="I'm assuming this is a unique hash for the message.")
    received_dtime = models.DateTimeField(auto_now_add=True,
        help_text="Time of initial receiving.")
    is_order = models.BooleanField(
        help_text="If True, this is an order. If False, this is history.")
    message = models.TextField(
        help_text="Full JSON representation of the message.")

    class Meta(object):
        verbose_name = "UUDIF Message"
        verbose_name_plural = "UUDIF Messages"


class SeenOrders(models.Model):
    """
    Track which orders we've seen in this last cycle.
    """
    id = models.BigIntegerField(primary_key=True,
        help_text="Order ID")
    region_id = models.PositiveIntegerField(
        help_text="Region ID of seen order")
    type_id = models.PositiveIntegerField(
        help_text="Type ID of seen order")

    class Meta(object):
        verbose_name = "Seen Order"
        verbose_name_plural = "Seen Orders"


class EmdrStats(models.Model):
    """
    Tracking statistics for EMDR messages
    """
    status_type = models.SmallIntegerField(
        help_text="Message type for statistics")
    status_count = models.PositiveIntegerField(
        help_text="Count of messages of specific type")
    message_timestamp = models.DateTimeField(auto_now_add=True, db_index=True,
        help_text="When the stats were counted for this entry")

    class Meta(object):
        verbose_name = "Message Statistics Data"
        verbose_name_plural = "Message Statistics Data"


class EmdrStatsWorking(models.Model):
    """
    Tracking statistics for EMDR messages
    """
    status_type = models.SmallIntegerField(
        help_text="Message type for statistics")

    class Meta(object):
        verbose_name = "Message Statistics Live Data"
        verbose_name_plural = "Message Statistics Live Data"


class ItemRegionStat(models.Model):
    """
    Stats for items on a per region basis
    processed when new orders come in during warehousing
    """
    
    mapregion = models.ForeignKey('eve_db.MapRegion', db_index=True, help_text="FK to region table")
    invtype = models.ForeignKey('eve_db.InvType', db_index=True, help_text="FK to type table")
    buymean = models.FloatField(help_text="Mean of buy price")
    buyavg = models.FloatField(help_text="Average of buy price")
    sellmean = models.FloatField(help_text="Mean of sell price")
    sellavg = models.FloatField(help_text="Avg of sell price")
    buymedian = models.FloatField(help_text="Median of buy price")
    sellmedian = models.FloatField(help_text="Median of sell price")
    buyvolume = models.BigIntegerField(help_text="total volume traded")
    sellvolume = models.BigIntegerField(help_text="total volume traded")
    buy_95_percentile = models.FloatField(help_text="95th % of buy orders")
    sell_95_percentile = models.FloatField(help_text="95th % of sell orders")
    lastupdate = models.DateTimeField(blank=True, null=True, help_text="Date the stats were updated")

    class Meta(object):
        verbose_name = "Stat Data"
        verbose_name_plural = "Stats Data"


class ItemRegionStatHistory(models.Model):
    """
    Stats for items on a per region basis
    processed when new orders come in during warehousing
    """

    mapregion = models.ForeignKey('eve_db.MapRegion', db_index=True, help_text="FK to region table")
    invtype = models.ForeignKey('eve_db.InvType', db_index=True, help_text="FK to type table")
    buymean = models.FloatField(help_text="Mean of buy price")
    buyavg = models.FloatField(help_text="Average of buy price")
    sellmean = models.FloatField(help_text="Mean of sell price")
    sellavg = models.FloatField(help_text="Avg of sell price")
    buymedian = models.FloatField(help_text="Median of buy price")
    sellmedian = models.FloatField(help_text="Median of sell price")
    buyvolume = models.BigIntegerField(help_text="total volume traded")
    sellvolume = models.BigIntegerField(help_text="total volume traded")
    buy_95_percentile = models.FloatField(help_text="95th % of buy orders")
    sell_95_percentile = models.FloatField(help_text="95th % of sell orders")
    date = models.DateTimeField(blank=True, null=True, help_text="Date the stats were inserted")

    class Meta(object):
        verbose_name = "Stat History Data"
        verbose_name_plural = "Stat History Data"


class History(models.Model):
    """
    All the history data stored as a compressed JSON message in region/typeID groups
    """

    id = models.CharField(max_length=255, primary_key=True,
        help_text="Primary key, based on UUID")
    mapregion = models.ForeignKey('eve_db.MapRegion', db_index=True,
        help_text="Region ID the order originated from.")
    invtype = models.ForeignKey('eve_db.InvType', db_index=True,
        help_text="The Type ID of the item in the order.")
    history_data = models.TextField(
        help_text="Compressed zlib data of the JSON message for history")

    class Meta(object):
        verbose_name = "History Data"
        verbose_name_plural = "History Data"


class OrderHistory(models.Model):
    """
    Post-processed history
    """

    mapregion = models.ForeignKey('eve_db.MapRegion', db_index=True,
        help_text="Region ID the order originated from.")
    invtype = models.ForeignKey('eve_db.InvType', db_index=True,
        help_text="The Type ID of the item in the order.")
    date = models.DateTimeField(help_text="Date of the data")
    numorders = models.PositiveIntegerField(help_text="number of transactions for this item/region")
    low = models.FloatField(help_text="low price of orders for this item/region")
    high = models.FloatField(help_text="high price of orders for this item/region")
    mean = models.FloatField(help_text="mean price of orders for this item/region")
    quantity = models.BigIntegerField(help_text="quantity of item sold for this item/region")


class OrdersWarehouse(models.Model):
    """
    A parsed order message with the details broken out into the various fields.
    This represents a single line in a UUDIF rowset.
    """

    mapregion = models.ForeignKey('eve_db.MapRegion', db_index=True,
        help_text="Region ID the order originated from.")
    invtype = models.ForeignKey('eve_db.InvType', db_index=True,
        help_text="The Type ID of the item in the order.")
    stastation = models.ForeignKey('eve_db.StaStation', db_index=True,
        help_text="The station that this order is in.")
    mapsolarsystem = models.ForeignKey('eve_db.MapSolarSystem',
        help_text="ID of the solar system the order is in.")
    generated_at = models.DateTimeField(blank=True, null=True,
        help_text="When the market data was generated on the user's machine.")
    price = models.FloatField(
        help_text="Item price, as reported in the message.")
    volume_entered = models.PositiveIntegerField(
        help_text="Number of items initially put up for sale.")
    order_range = models.IntegerField(
        help_text="How far the order is visible.  32767 = region-wide")
    id = models.BigIntegerField(primary_key=True,
        help_text="Unique order ID from EVE for this order.")
    is_bid = models.BooleanField(
        help_text="If True, this is a buy order. If False, this is a sell order.")
    issue_date = models.DateTimeField(
        help_text="When the order was issued.")
    duration = models.PositiveSmallIntegerField(
        help_text="The duration of the order, in days.")
    is_suspicious = models.BooleanField(
        help_text="If this is True, we have reason to question this order's validity")
    message_key = models.CharField(max_length=255,
        help_text="The unique hash of the market message.")
    uploader_ip_hash = models.CharField(max_length=255, db_index=True,
        help_text="The unique hash for the person who uploaded this message.")

    class Meta(object):
        verbose_name = "Market Data"
        verbose_name_plural = "Market Data"

class ActiveOrdersManager(models.Manager):
    """
    Custom manager that only returns active orders.
    
    Example: Get all active orders --> Orders.active.all()
    """
    def get_query_set(self):
        return super(LiveOrdersManager, self).get_query_set().filter(is_active=True)

class ArchivedOrdersManager(models.Manager):
    """
    Custom manager that only returns archived orders.
    
    Example: Get all archived orders --> Orders.archived.all()
    """
    def get_query_set(self):
        return super(HistoryOrdersManager, self).get_query_set().filter(live=False)

class Orders(models.Model):
    """
    A parsed order message with the details broken out into the various fields.
    This represents a single line in a UUDIF rowset.
    """

    generated_at = models.DateTimeField(blank=True, null=True,
        help_text="When the market data was generated on the user's machine.")
    mapregion = models.ForeignKey('eve_db.MapRegion', db_index=True,
        help_text="Region ID the order originated from.")
    invtype = models.ForeignKey('eve_db.InvType', db_index=True,
        help_text="The Type ID of the item in the order.")
    price = models.FloatField(
        help_text="Item price, as reported in the message.")
    volume_remaining = models.PositiveIntegerField(
        help_text="Number of remaining items for sale.")
    volume_entered = models.PositiveIntegerField(
        help_text="Number of items initially put up for sale.")
    minimum_volume = models.PositiveIntegerField(
        help_text="Minimum volume before the order finishes.")
    order_range = models.IntegerField(
        help_text="How far the order is visible.  32767 = region-wide")
    id = models.BigIntegerField(primary_key=True,
        help_text="Unique order ID from EVE for this order.")
    is_bid = models.BooleanField(
        help_text="If True, this is a buy order. If False, this is a sell order.")
    issue_date = models.DateTimeField(
        help_text="When the order was issued.")
    duration = models.PositiveSmallIntegerField(
        help_text="The duration of the order, in days.")
    stastation = models.ForeignKey('eve_db.StaStation', db_index=True,
        help_text="The station that this order is in.")
    mapsolarsystem = models.ForeignKey('eve_db.MapSolarSystem',
        help_text="ID of the solar system the order is in.")
    is_suspicious = models.BooleanField(
        help_text="If this is True, we have reason to question this order's validity")
    message_key = models.CharField(max_length=255,
        help_text="The unique hash that of the market message.")
    uploader_ip_hash = models.CharField(max_length=255, db_index=True,
        help_text="The unique hash for the person who uploaded this message.")
    live = models.BooleanField(help_text="is this a live order or is it history")

    # Managers
    objects = models.Manager()
    active = ActiveOrdersManager()
    archived = ArchivedOrdersManager()
    
    class Meta(object):
        verbose_name = "Market Order"
        verbose_name_plural = "Market Orders"
