from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.common.views',
    # Home
    url(r'^$', 'home', name = 'home'),
    url(r'^stats/(?P<region_id>[0-9]+)/', 'stats_json', name = 'home_stats_json'),

    # Search
    url(r'^search/', 'search', name = 'search'),

    # Live search
    url(r'^live_search/', 'live_search', name = 'live_search'),
    
    # About page
    url(r'^about/', 'about_page', name='about_page'),
)