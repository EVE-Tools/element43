from django.conf.urls import patterns, include, url
from django.contrib import admin

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
    
    # Authentication and registration
    url(r'', include('apps.auth.urls')),
    
    # Market data
    url(r'^market/', include('apps.market_data.urls')),
    
    # Account management
    url(r'^settings/', include('apps.user_settings.urls')),
    
    # Manufacturing
    url(r'^manufacturing/', include('apps.manufacturing.urls')),
)

#
# Administration views
#

urlpatterns += patterns('',     
    # Admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
