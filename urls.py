from django.conf.urls import patterns, include, url

# Womoobox URLs
womooboxpatterns = patterns('',
    url(r'^$',                 'womoobox.views.get_map'),
    url(r'^api/$',             'womoobox.api.api_index'),
    url(r'^api/moo/add',       'womoobox.api.moo_add'),
    url(r'^api/moo/get_lasts', 'womoobox.api.moo_get_lasts'),
    url(r'^api/moo/count',     'womoobox.api.moo_get_count'),
    url(r'^api/moo',           'womoobox.views.moo_get_form'),
    url(r'^api/key/add',       'womoobox.api.key_add'),
    url(r'^api/key/rename',    'womoobox.api.key_rename'),
)
