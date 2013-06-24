import django_filters

from apps.market_data.models import Orders, OrderHistory, ItemRegionStat


class OrdersFilter(django_filters.FilterSet):
    class Meta:
        model = Orders

        fields = ['mapregion',
                  'invtype',
                  'minimum_volume',
                  'is_bid',
                  'stastation',
                  'mapsolarsystem',
                  'is_suspicious']


class ItemRegionStatFilter(django_filters.FilterSet):
    class Meta:
        model = ItemRegionStat

        fields = ['mapregion',
                  'invtype']


class OrderHistoryFilter(django_filters.FilterSet):
    class Meta:
        model = OrderHistory

        fields = ['mapregion',
                  'invtype']
