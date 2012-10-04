from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.common.views',
    # Home
    url(r'^$', 'home', name = 'home'),
    url(r'^stats/$', 'stats', name = 'home_stats_panel'),

    # Search
    url(r'^search/', 'search', name = 'search'),

    # Live search
    url(r'^live_search/', 'live_search', name = 'live_search'),
)