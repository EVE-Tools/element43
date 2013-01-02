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

    # Manufacturing
    url(r'^manufacturing/', include('apps.manufacturing.urls')),

    #
    # SSL URLs
    #

    # Authentication and registration
    url(r'^secure/', include('apps.auth.urls')),

    # Dashboard
    url(r'^secure/dashboard/', include('apps.dashboard.urls')),

    # Wallet
    url(r'^secure/wallet/', include('apps.wallet.urls')),

    # Account management
    url(r'^secure/settings/', include('apps.user_settings.urls')),
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
