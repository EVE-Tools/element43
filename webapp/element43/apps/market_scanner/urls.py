from django.conf.urls import patterns, url

urlpatterns = patterns('apps.market_scanner.views',
	# Scanners
    url(r'^random/$', 'random', name='scanner_random'),
    url(r'^region/$', 'region', name='scanner_region'),
)