from django.conf.urls import patterns, url

urlpatterns = patterns('apps.dashboard.views',
    #
    # Account management
    #

    # Settings
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^journal/$', 'journal_json', name='journal_json'),
    url(r'^char_sheet/(?P<char_id>[0-9]+)/$', 'char_sheet', name='char_sheet')

)
