from django.conf.urls import patterns, url

from gamequest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^system/(?P<system_id>\d+)$', views.systemInfo, name='system'), 
    url(r'^system/(?P<system_id>\d+)/games$', views.systemGames, name='system_games'), 
    url(r'^game/(?P<game_id>\d+)$', views.gameInfo, name='game'), 
    url(r'^achievement/add_achievement$', views.AddAchievementView.as_view(), name='add_achievement'), 
    url(r'^contest/(?P<contest_id>\d+)$', views.contestInfo, name='contest'), 
    url(r'^contest/(?P<contest_id>\d+)/list/viewall$', views.contestAchievementListsAll, name='contest_achievement_list_viewall'), 
    url(r'^contest/(?P<contest_id>\d+)/participants$', views.contestParticipantList, name='contest_participant_list'), 
    url(r'^contest/(?P<contest_id>\d+)/list/create$',views.achievementListCreate, name='create_achievement_list'),
    url(r'^contest/(?P<contest_id>\d+)/list/edit/(?P<achievement_list_id>\d+)/$',views.achievementListEdit, name='edit_achievement_list'),
    url(r'^contest/(?P<contest_id>\d+)/list/edit_list/(?P<achievement_list_id>\d+)$',views.achievementListAddAchievements, name='edit_achievement_list_add'),
    url(r'^contest/(?P<contest_id>\d+)/list/remove_achievement/(?P<achievement_list_id>\d+)/(?P<achievement_id>\d+)$',views.achievementListRemoveAchievement, name='edit_achievement_list_remove'),
    url(r'^contest/(?P<contest_id>\d+)/list/remove_achievement_list/(?P<achievement_list_id>\d+)/$',views.achievementListRemove, name='remove_achievement_list'),
    url(r'^contest/(?P<contest_id>\d+)/user/(?P<requested_username>\w+)$', views.contestParticipantProfile, name='contest_participant'), 
    url(r'^user/(?P<requested_username>\w+)$', views.userProfile, name="user_profile"), 
    url(r'^auth/login$', 'django.contrib.auth.views.login', {'template_name': 'gamequest/login.html'}, name="login"),
    url(r'^auth/user_redirect$',views.userProfileRedirect, name="user_profile_redirect"),
    url(r'^auth/logout$','django.contrib.auth.views.logout', {'template_name': 'gamequest/logged_out.html'}, name="logout"),
)
