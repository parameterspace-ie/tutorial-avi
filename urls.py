from avi import views
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),

    url(r'^(?P<fib>[0-9]+)$', views.create, name='create'),
)
