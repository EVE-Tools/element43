from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.auth.views',
    #
    # Authentication and Registration URLs
    #

    # Registration
    url(r'^register/activate/(?P<key>[a-zA-Z0-9]+)/$', 'activate', name='activate_account'),
    url(r'^register/$', 'register', name='registration'),

    # Password reset
    url(r'^register/reset_password/$', 'reset_password', name='reset_password'),

    # Login
    url(r'^login/$', 'login', name='login'),
    # Logout
    url(r'^logout/$', 'logout', name='logout'),
)
