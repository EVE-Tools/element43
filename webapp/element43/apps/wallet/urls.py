from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.wallet.views',
    url(r'^$', 'wallet', name='wallet_overview')
)
