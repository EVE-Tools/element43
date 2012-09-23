from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    
	#
	# Base URLs
	#

	# Home
    url(r'^$', 'apps.market_data.views.base.home'),

	# Search
	url(r'^search/', 'apps.market_data.views.base.search'),

	# Live search
	url(r'^live_search/(?P<query>[a-zA-Z]+)', 'apps.market_data.views.base.live_search'),
		
	#
	# Authentication and Registration URLs
	#
		
	# Registration
	url(r'^register/activate/(?P<key>[a-zA-Z0-9]+)/$', 'apps.market_data.views.auth.auth.activate'),
	url(r'^register/$', 'apps.market_data.views.auth.auth.register'),
    
    # Password reset
    url(r'^register/reset_password/$', 'apps.market_data.views.auth.auth.reset_password'),
		
	# Login
	url(r'^login/$', 'apps.market_data.views.auth.auth.login'),
	# Logout
	url(r'^logout/$', 'apps.market_data.views.auth.auth.logout'),
		
	#
	# Market URLs
	#

    # Quicklook
    url(r'^market/(?P<type_id>[0-9]+)/', 'apps.market_data.views.market.market.quicklook'),
	url(r'^market/region/(?P<region_id>[0-9]+)/(?P<type_id>[0-9]+)/', 'apps.market_data.views.market.market.quicklook_region'),
		
	# History JSON
	url(r'^market/history/(?P<region_id>[0-9]+)/(?P<type_id>[0-9]+)/', 'apps.market_data.views.market.market.history_json'),

	# Market browser
	url(r'^market/browse/(?P<group>[0-9]+)/', 'apps.market_data.views.market.browser.browser'),
	url(r'^market/browse/', 'apps.market_data.views.market.browser.browser'),
		
	# Scanners
    url(r'^market/scanner/random/', 'apps.market_data.views.market.scanners.random'),
	url(r'^market/scanner/region/', 'apps.market_data.views.market.scanners.region'),
		
	#
	# Trading URLs
	#
		
	# Station ranking
	url(r'^trading/station/ranking/', 'apps.market_data.views.trading.station.ranking'),
		
	#
	# Administration URLs
	#
		
    # Admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
