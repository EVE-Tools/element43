from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.user_settings.views',
    #
    # Account management
    #
    
    # Settings
    url(r'^/', 'profile', name = 'settings'),
    url(r'^profile/$', 'profile', name = 'settings'),
    url(r'^characters/$', 'characters', name = 'manage_characters'),
    url(r'^characters/remove/(?P<char_id>[0-9]+)/$', 'remove_character', name = 'remove_character'),
    url(r'^api/key/$', 'api_key', name = 'manage_api_keys'),
    url(r'^api/key/remove/(?P<apikey_id>[0-9]+)/$', 'remove_api_key', name = 'remove_api_key'),
    url(r'^api/character/(?P<api_id>[0-9]+)/(?P<api_verification_code>[a-zA-Z0-9]+)/$', 'api_character', name = 'add_characters'),

)
