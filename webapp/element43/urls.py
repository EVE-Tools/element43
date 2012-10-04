from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

# Custom error handlers
handler403 = 'apps.market_data.views.errors.handler_403'
handler404 = 'apps.market_data.views.errors.handler_404'
handler500 = 'apps.market_data.views.errors.handler_500'

#
# market_data
#

urlpatterns = patterns('apps.market_data.views',
    
    #
    # Base URLs
    #

    # Home
    url(r'^$', 'base.home', name = 'home'),
    url(r'^stats/$', 'base.stats', name = 'home_stats_panel'),

    # Search
    url(r'^search/', 'base.search', name = 'search'),

    # Live search
    url(r'^live_search/', 'base.live_search', name = 'live_search'),
        
    #
    # Authentication and Registration URLs
    #
        
    # Registration
    url(r'^register/activate/(?P<key>[a-zA-Z0-9]+)/$', 'auth.auth.activate', name = 'activate_account'),
    url(r'^register/$', 'auth.auth.register', name = 'registration'),
    
    # Password reset
    url(r'^register/reset_password/$', 'auth.auth.reset_password', name = 'reset_password'),
        
    # Login
    url(r'^login/$', 'auth.auth.login', name = 'login'),
    # Logout
    url(r'^logout/$', 'auth.auth.logout', name = 'logout'),
    
    #
    # Account management
    #
    
    # Settings
    url(r'^settings/$', 'settings.profile', name = 'settings'),
    url(r'^settings/profile/$', 'settings.profile', name = 'settings'),
    url(r'^settings/characters/$', 'settings.characters', name = 'manage_characters'),
    url(r'^settings/characters/remove/(?P<char_id>[0-9]+)/$', 'settings.remove_character', name = 'remove_character'),
    url(r'^settings/api/key/$', 'settings.api_key', name = 'manage_api_keys'),
    url(r'^settings/api/key/remove/(?P<apikey_id>[0-9]+)/$', 'settings.remove_api_key', name = 'remove_api_key'),
    url(r'^settings/api/character/(?P<api_id>[0-9]+)/(?P<api_verification_code>[a-zA-Z0-9]+)/$', 'settings.api_character', name = 'add_characters'),
    
    #
    # Market URLs
    #

    # Quicklook
    url(r'^market/(?P<type_id>[0-9]+)/', 'market.market.quicklook', name = 'quicklook'),
    url(r'^market/tab/ask/(?P<type_id>[0-9]+)/(?P<min_sec>[0-9]+)/(?P<max_age>[0-9]+)/', 'market.market.quicklook_ask_filter', name = 'quicklook_filter_tab_ask'),
    url(r'^market/tab/bid/(?P<type_id>[0-9]+)/(?P<min_sec>[0-9]+)/(?P<max_age>[0-9]+)/', 'market.market.quicklook_bid_filter', name = 'quicklook_filter_tab_bid'),
    url(r'^market/region/(?P<region_id>[0-9]+)/(?P<type_id>[0-9]+)/', 'market.market.quicklook_region', name = 'quicklook_region'),
        
    # History JSON
    url(r'^market/history/(?P<region_id>[0-9]+)/(?P<type_id>[0-9]+)/', 'market.market.history_json', name = 'quicklook_history_json'),

    # Market browser
    url(r'^market/browse/tree/(?P<group>[0-9]+)/$', 'market.browser.tree', name = 'browser_tree_group_json'),
    url(r'^market/browse/tree/$', 'market.browser.tree', name = 'browser_tree'),
    
    url(r'^market/browse/(?P<group>[0-9]+)/', 'market.browser.browser', name = 'browser_preload'),
    url(r'^market/browse/panel/(?P<group>[0-9]+)/', 'market.browser.panel', name = 'browser_panel'),
    url(r'^market/browse/', 'market.browser.browser', name = 'browser'),
        
    # Scanners
    url(r'^market/scanner/random/', 'market.scanners.random', name = 'scanner_random'),
    url(r'^market/scanner/region/', 'market.scanners.region', name = 'scanner_region'),
        
    #
    # Trading URLs
    #
        
    # Station ranking
    url(r'^trading/station/ranking/', 'trading.station.ranking', name = 'station_ranking'),
)
        
#
# Administration views
#

urlpatterns += patterns('',     
    # Admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
