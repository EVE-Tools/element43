from django.conf.urls import patterns, url

urlpatterns = patterns('apps.market_browser.views',
    # Market browser
    url(r'^$', 'browser', name='browser'),
    url(r'^(?P<group>[0-9]+)/$', 'browser', name='browser_preload'),
    url(r'^panel/(?P<group>[0-9]+)/$', 'panel', name='browser_panel'),
)