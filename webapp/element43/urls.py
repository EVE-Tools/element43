from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apps.market_data.views.home'),
    # url(r'^element43/', include('element43.foo.urls')),
    url(r'^market/scanner/random/', 'apps.market_data.scanners.random'),

		# Search
		url(r'^search/', 'apps.market_data.views.search'),

		# Live search
		url(r'^live_search/(?P<query>[a-zA-Z]+)', 'apps.market_data.views.live_search'),
		
		# Quicklook
		url(r'^market/(?P<type_id>[0-9]+)/', 'apps.market_data.views.quicklook'),
		
		# Market browser
		url(r'^browse/(?P<group>[0-9]+)/', 'apps.market_data.views.browser'),
		url(r'^browse/', 'apps.market_data.views.browser'),
		
    # Admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
