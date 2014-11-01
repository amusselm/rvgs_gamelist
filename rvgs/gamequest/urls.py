from django.conf.urls import patterns, url

from gamequest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^system/(?P<system_id>\d+)$', views.systemInfo, name='system'), 
)
