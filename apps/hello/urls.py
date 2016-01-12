from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.hello.views',
    url(r'(?P<pk>.*)/$', 'home', name="home-page"),
)
