from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.wallet.views',
    url(r'^$', 'wallet', name='wallet_overview'),

    # Type-based report
    url(r'^type/(?P<type_id>[0-9]+)/$', 'type', name='wallet_type'),

    # Active Orders
    url(r'^orders/active/$', 'active_orders', name='wallet_orders_active'),

    # Archived Orders
    url(r'^orders/archived/$', 'archived_orders', name='wallet_orders_archived'),

    # Journal
    url(r'^journal/$', 'journal', name='wallet_journal'),

    # Transactions
    url(r'^transactions/$', 'transactions', name='wallet_transactions')
)
