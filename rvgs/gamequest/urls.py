from django.conf.urls import patterns, url

from gamequest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^system/(?P<system_id>\d+)$', views.systemInfo, name='system'), 
    url(r'^system/(?P<system_id>\d+)/games$', views.systemGames, name='system_games'), 
    url(r'^game/(?P<game_id>\d+)$', views.gameInfo, name='game'), 
    url(r'^contest/(?P<contest_id>\d+)$', views.contestInfo, name='contest'), 
)
