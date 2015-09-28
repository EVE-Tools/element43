from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings

admin.autodiscover()

# Custom error handlers
handler403 = 'apps.common.views.handler_403'
handler404 = 'apps.common.views.handler_404'
handler500 = 'apps.common.views.handler_500'

#
# URLs for Element43
#

urlpatterns = patterns('',
    # Common URLs
    url(r'', include('apps.common.urls')),

    # Market data
    url(r'^market/', include('apps.market_data.urls')),

    # Quicklook
    url(r'^market/', include('apps.quicklook.urls')),

    # Tradefinder views
    url(r'^market/', include('apps.market_tradefinder.urls')),

    # Station views
    url(r'^market/trading/', include('apps.market_station.urls')),

    # Market browser
    url(r'^market/browse/', include('apps.market_browser.urls')),

    # Market scanners
    url(r'^market/scanner/', include('apps.market_scanner.urls')),

    # Legacy API
    url(r'^market/api/', include('apps.legacy_api.urls')),

    # Manufacturing
    #url(r'^manufacturing/', include('apps.manufacturing.urls')),

    #
    # SSL URLs
    #

    # Authentication and registration
    url(r'^secure/', include('apps.authentication.urls')),

    # Dashboard
    url(r'^secure/dashboard/', include('apps.dashboard.urls')),

    # Wallet
    url(r'^secure/wallet/', include('apps.wallet.urls')),

    # Account management
    url(r'^secure/settings/', include('apps.user_settings.urls')),


    #
    # REST API
    #

    url(r'^api/', include('apps.rest_api.urls')),
)

#
# Administration views
#

if settings.ADMIN_ENABLED:
    urlpatterns += patterns('',
        # Admin documentation:
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)),
    )
