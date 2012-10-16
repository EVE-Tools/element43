from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.manufacturing.views',
    url(r'^calculator/$', 'calculator.select_blueprint', name='manufacturing_select_blueprint'),

    # if you change the following url don't forget to update they in manufacturing.js!
    url(r'^calculator/(?P<blueprint_type_id>[0-9]+)/$', 'calculator.calculator', name='manufacturing_calculator'),
    url(r'^blueprint_search/$', 'base.blueprint_search', name="manufacturing_blueprint_search"),
)