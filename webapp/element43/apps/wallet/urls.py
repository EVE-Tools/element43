from django.conf.urls import patterns, url

urlpatterns = patterns('apps.wallet.views',
    url(r'^$', 'wallet', name='wallet_overview'),

    # Type-based report
    url(r'^type/(?P<type_id>[0-9]+)/$', 'type', name='wallet_type'),

    # Active Orders
    url(r'^orders/active/$', 'active_orders', name='wallet_orders_active'),

    # Station Scanner
    url(r'^orders/active/scanner/(?P<station_id>[0-9]+)/$', 'station_scanner', name='wallet_station_scanner'),

    # Archived Orders
    url(r'^orders/archived/$', 'archived_orders', name='wallet_orders_archived'),

    # Journal
    url(r'^journal/(?P<char_id>[0-9]+)/$', 'journal', name='wallet_journal'),

    # Transactions
    url(r'^transactions/(?P<char_id>[0-9]+)/$', 'transactions', name='wallet_transactions')
)
