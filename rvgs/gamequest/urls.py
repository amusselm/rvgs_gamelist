from django.conf.urls import patterns, url

from gamequest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^system/(?P<system_id>\d+)$', views.systemInfo, name='system'), 
    url(r'^system/(?P<system_id>\d+)/games$', views.systemGames, name='system_games'), 
    url(r'^game/(?P<game_id>\d+)$', views.gameInfo, name='game'), 
    url(r'^contest/(?P<contest_id>\d+)$', views.contestInfo, name='contest'), 
    url(r'^contest/(?P<contest_id>\d+)/participants$', views.contestParticipantList, name='contest_participant_list'), 
    url(r'^contest/(?P<contest_id>\d+)/list/create$',views.achievementListEdit, name='create_achievement_list'),
    url(r'^contest/(?P<contest_id>\d+)/user/(?P<requested_username>\w+)$', views.contestParticipantProfile, name='contest_participant'), 
    url(r'^user/(?P<requested_username>\w+)$', views.userProfile, name="user_profile"), 
    url(r'^auth/login$', 'django.contrib.auth.views.login', {'template_name': 'gamequest/login.html'}, name="login"),
    url(r'^auth/user_redirect$',views.userProfileRedirect, name="user_profile_redirect"),
    url(r'^auth/logout$','django.contrib.auth.views.logout', {'template_name': 'gamequest/logged_out.html'}, name="logout"),
)
