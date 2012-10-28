from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.wallet.views',
    url(r'^$', 'wallet', name='wallet_overview'),
    url(r'^type/(?P<type_id>[0-9]+)/$', 'type', name='wallet_type'),
)
