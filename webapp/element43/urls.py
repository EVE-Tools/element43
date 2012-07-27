from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apps.market_data.views.home'),
    # url(r'^element43/', include('element43.foo.urls')),
    url(r'^market/scanner/', 'apps.market_data.scanners.random'),

		# live search
		url(r'live_search/(?P<query>[a-zA-Z]+)', 'apps.market_data.views.live_search'),

    # admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
