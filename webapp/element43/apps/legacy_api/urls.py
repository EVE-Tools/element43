from django.conf.urls import patterns, url

urlpatterns = patterns('apps.legacy_api.views',
    #
    # API URLs
    #

    # legacy marketstat
    url(r'^ec_marketstat/$', 'marketstat.legacy_marketstat', name='legacy_marketstat'),

    # new API
    url(r'^marketstat/$', 'marketstat.marketstat', name='marketstat'),
)