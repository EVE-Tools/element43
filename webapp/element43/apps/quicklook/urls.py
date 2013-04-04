from django.conf.urls import patterns, url

urlpatterns = patterns('apps.quicklook.views',
    # Quicklook
    url(r'^(?P<type_id>[0-9]+)/$', 'quicklook', name='quicklook'),
    url(r'^tab/regions/(?P<type_id>[0-9]+)/$', 'quicklook_tab_regions', name='quicklook_tab_regions'),
    url(r'^tab/systems/(?P<region_id>[0-9]+)/(?P<type_id>[0-9]+)/$', 'quicklook_tab_systems', name='quicklook_tab_systems'),
    url(r'^tab/ask/(?P<type_id>[0-9]+)/(?P<min_sec>[0-9]+)/(?P<max_age>[0-9]+)/$', 'quicklook_ask_filter', name='quicklook_filter_tab_ask'),
    url(r'^tab/bid/(?P<type_id>[0-9]+)/(?P<min_sec>[0-9]+)/(?P<max_age>[0-9]+)/$', 'quicklook_bid_filter', name='quicklook_filter_tab_bid'),
    url(r'^region/(?P<region_id>[0-9]+)/(?P<type_id>[0-9]+)/$', 'quicklook_region', name='quicklook_region'),
)
