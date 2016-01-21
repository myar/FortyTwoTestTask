from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.hello.views',
    url(r'^editdata/(?P<pk>.*)/$', 'edit_data', '', name="edit-data"),
    url(r'^store/$', 'http_request_storage', '', name="middleware-storage"),
    url(r'^(?P<pk>\d+)/$', 'home', name="home-page"),
    url(r'^$', 'home', name="home"),
)
