from django.conf.urls import patterns, url

urlpatterns = patterns('apps.market_data.views',
    # History JSON
    url(r'^history/(?P<type_id>[0-9]+)/$', 'history_compare_json', name='quicklook_history_compare_json'),
    url(r'^history/(?P<region_id>[0-9]+)/(?P<type_id>[0-9]+)/$', 'history_json', name='quicklook_history_json'),
)
