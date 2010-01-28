from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('d51.django.apps.sharing.views',
    url(r'^(?P<service_name>\w+)/$', 'share_url', name='share_url'),
)
