from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

handler403 = 'apps.market_data.views.errors.handler_403'
handler404 = 'apps.market_data.views.errors.handler_404'
handler500 = 'apps.market_data.views.errors.handler_500'

urlpatterns = patterns('',
    
	#
	# Base URLs
	#

	# Home
    url(r'^$', 'apps.market_data.views.base.home'),
	url(r'^stats/$', 'apps.market_data.views.base.stats'),

	# Search
	url(r'^search/', 'apps.market_data.views.base.search'),

	# Live search
	url(r'^live_search/', 'apps.market_data.views.base.live_search'),
		
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
	# Account management
	#
	
	# Settings
	url(r'^settings/$', 'apps.market_data.views.settings.profile'),
	url(r'^settings/profile/$', 'apps.market_data.views.settings.profile'),
	url(r'^settings/characters/$', 'apps.market_data.views.settings.characters'),
	url(r'^settings/characters/remove/(?P<char_id>[0-9]+)/$', 'apps.market_data.views.settings.remove_character'),
	url(r'^settings/api/key/$', 'apps.market_data.views.settings.api_key'),
	url(r'^settings/api/key/remove/(?P<apikey_id>[0-9]+)/$', 'apps.market_data.views.settings.remove_api_key'),
	url(r'^settings/api/character/(?P<api_id>[0-9]+)/(?P<api_verification_code>[a-zA-Z0-9]+)/$', 'apps.market_data.views.settings.api_character'),
	
		
	#
	# Market URLs
	#

    # Quicklook
    url(r'^market/(?P<type_id>[0-9]+)/', 'apps.market_data.views.market.market.quicklook'),
	url(r'^market/tab/ask/(?P<type_id>[0-9]+)/(?P<min_sec>[0-9]+)/(?P<max_age>[0-9]+)/', 'apps.market_data.views.market.market.quicklook_ask_filter'),
	url(r'^market/tab/bid/(?P<type_id>[0-9]+)/(?P<min_sec>[0-9]+)/(?P<max_age>[0-9]+)/', 'apps.market_data.views.market.market.quicklook_bid_filter'),
	url(r'^market/region/(?P<region_id>[0-9]+)/(?P<type_id>[0-9]+)/', 'apps.market_data.views.market.market.quicklook_region'),
		
	# History JSON
	url(r'^market/history/(?P<region_id>[0-9]+)/(?P<type_id>[0-9]+)/', 'apps.market_data.views.market.market.history_json'),

	# Market browser
	url(r'^market/browse/tree/(?P<group>[0-9]+)/$', 'apps.market_data.views.market.browser.tree'),
	url(r'^market/browse/tree/$', 'apps.market_data.views.market.browser.tree'),
	
	url(r'^market/browse/(?P<group>[0-9]+)/', 'apps.market_data.views.market.browser.browser'),
	url(r'^market/browse/panel/(?P<group>[0-9]+)/', 'apps.market_data.views.market.browser.panel'),
	url(r'^market/browse/', 'apps.market_data.views.market.browser.browser'),
		
	# Scanners
    url(r'^market/scanner/random/', 'apps.market_data.views.market.scanners.random'),
	url(r'^market/scanner/region/', 'apps.market_data.views.market.scanners.region'),
		
	#
	# Trading URLs
	#
	
	# Station
	#url(r'^trading/station/(?P<station_id>[0-9]+)/', 'apps.market_data.views.trading.station.margins'),
		
	# Station ranking
	url(r'^trading/station/ranking/', 'apps.market_data.views.trading.station.ranking'),
	
	#
	# Manufacturing URLs
	#
	url(r'^manufacturing/calculator/$', 'apps.manufacturing.views.calculator.select_blueprint', name='manufacturing_select_blueprint'),
	url(r'^manufacturing/calculator/(?P<blueprint_type_id>[0-9]+)/$', 'apps.manufacturing.views.calculator.calculator', name='manufacturing_calculator'),
	url(r'^manufacturing/blueprint_search/$', 'apps.manufacturing.views.base.blueprint_search'),
	
	#
	# Administration URLs
	#
		
    # Admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
