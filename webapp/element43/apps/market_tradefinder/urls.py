from django.conf.urls import patterns, url

urlpatterns = patterns('apps.market_tradefinder.views',

    #
    # Tradefinder URLs
    #

    # Tradefinder root
    url(r'^tradefinder/$', 'tradefinder', name='tradefinder'),

    # Region name JSON
    url(r'^tradefinder/regions/$', 'region_json', name='tradefinder_region_json'),
)
