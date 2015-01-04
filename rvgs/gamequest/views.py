from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from models import *
from gamequest.forms import *

# Create your views here.
def index(request):
    return render(request, 'gamequest/base.html')

def systemInfo(request, system_id):
    """
    Display the information for a given games system
    """
    try:
        system = System.objects.get(pk=system_id)
    except System.DoesNotExist:
        raise Http404
    else:
        availableEmulators = System.objects.filter(emulating=system)
        context =  {'system':system,
            'available_emulators':availableEmulators,}    
    return render(request,'gamequest/system.html',context)

def systemGames(request, system_id):
    """
    Display a list of games that have been ported to this system
    """
    try:
        system = System.objects.get(pk=system_id)
    except System.DoesNotExist:
        raise Http404
    else:
        if(system.emulated):
            targetSystem = system.emulating
        else:
            targetSystem = system    
            ports = Game.objects.filter(ports=targetSystem)
            context = {'system':system,'ports':ports}
    return render(request,'gamequest/system_gamelist.html',context)

def gameInfo(request, game_id):
    """
    Display information about a game
    """
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404
    else:
        context = {'game':game,}
    return render(request,'gamequest/game.html',context)

def contestInfo(request, contest_id):
    """
    Display information about a given contest
    """
    try:
        contest = Contest.objects.get(pk=contest_id)
    except Contest.DoesNotExist:
        raise Http404
    else:
        recent_unlocks = Unlock.objects.filter(contest__id = contest_id)
        recent_unlocks.order_by('timestamp')[:10]
        context = {'contest':contest,'recent_unlocks':recent_unlocks,} 
    return render(request,'gamequest/contest.html',context)

def contestParticipantList(request, contest_id):
    """
    Display a list of all participants in a given contest
    """
    try:
        contest = Contest.objects.get(pk=contest_id)
    except Contest.DoesNotExist:
        raise Http404
    else:
        context = {'contest':contest,}
    return render (request, 'gamequest/contest_participant_list.html',context)

def contestAchievementListsAll(request, contest_id):
    """
    Display a list of all achievement lists assoicated with a contest
    """
    try:
        contest = Contest.objects.get(pk=contest_id)
    except Contest.DoesNotExist:
        raise Http404
    else:
        achievement_lists = AchievementList.objects.filter(contest__id = contest.id)
        context = {'contest':contest,'achievement_lists':achievement_lists,}
        return render(request,'gamequest/contest_achievement_list.html',context)
        

def contestParticipantProfile(request, contest_id, requested_username):
    """
    Display information about a users's participation in a given contest
    """
    try:
        contest = Contest.objects.get(pk=contest_id)
        user = User.objects.get(username=requested_username)
    except Contest.DoesNotExist:
        raise Http404
    else:
        unlocks = Unlock.objects.filter(contest__id = contest.id).filter(user=user)
        achievement_lists = AchievementList.objects.filter(contest__id = contest.id).filter(owner=user)
        context = {'contest':contest,
           'participant':user, 
           'unlocks':unlocks,
           'achievement_lists':achievement_lists}
    return render(request,'gamequest/contest_participant.html',context)
    

def userProfile(request, requested_username):
    """
    Display a user's profile page
    """
    try:
        user = User.objects.get(username=requested_username)
    except User.DoesNotExist:
        raise Http404
    else:
        upcoming_contests = Contest.objects.filter(participants=user).filter(upcoming=True)
        active_contests = Contest.objects.filter(participants=user).filter(active=True)
        archive_contests = Contest.objects.filter(participants=user).filter(archive=True)
        context = {'participant':user,
           'upcoming':upcoming_contests,
           'active':active_contests,
           'archive':archive_contests,}
    return render(request,'gamequest/user.html',context)

def userProfileRedirect(request):
    """
    Redirect to the user profile for the logged in user. If the user is not logged in,
    redirect to the login page. 
    """
    if (request.user.is_authenticated()):
        return redirect('user_profile', requested_username=request.user.get_username())
    else:
        return redirect('login')


@login_required 
def achievementListEdit(request,contest_id,achievement_list_id):
    """
    Proscesses the form when the user edits an Achievement Lists's name or 
    description. Or displays the form in the first place in the event of a GET request
    """
    try:
        contest = Contest.objects.get(pk=contest_id)
    except Contest.DoesNotExist:
        raise Http404
    if(achievement_list_id != None):
        try: 
            achievement_list = AchievementList.objects.get(pk=achievement_list_id)
        except AchievementList.DoesNotExist: 
            raise HTTP404

    if request.method == 'POST':
        form = AchievementListForm(request.POST,instance=achievement_list)
        if form.is_valid():
            if (request.user == achievement_list.owner and contest == achievement_list.contest):
                new_list = form.save()
    else:
        form = AchievementListForm(instance=achievement_list)
    
    context = { 'form':form, 
                'contest':contest, 
                'achievement_list':achievement_list,} 
    return render(request,'gamequest/edit_achievement_list.html',context)    

@login_required
def achievementListCreate(request,contest_id):
    """A view to create a new achievement list for a particular contest"""
    create = True
    try:
        contest = Contest.objects.get(pk=contest_id)
    except Contest.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = AchievementListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.owner = request.user 
            new_list.contest = contest
            new_list.save()
            return redirect('edit_achievement_list',contest_id,new_list.id)
    else:
        form = AchievementListForm()
    context = { 'form':form, 'contest':contest, 'create':create} 
    return render(request,'gamequest/edit_achievement_list.html',context)    

@login_required 
def achievementListRemoveAchievement(request,contest_id,achievement_list_id,achievement_id):
    """
    Gives the user a confirmation page to remove a specific achievement from a list, or
    if it receives a POSt requrest, does the removal
    """
    try:
        contest = Contest.objects.get(pk=contest_id)
    except Contest.DoesNotExist:
        raise Http404
    try: 
        achievement_list = AchievementList.objects.get(pk=achievement_list_id)
    except AchievementList.DoesNotExist: 
        raise HTTP404
    try:
        achievement = Achievement.objects.get(pk=achievement_id)
    except Achievement.DoesNotExist:
        raise HTTP404

    if request.method == 'POST':
        if (request.user == achievement_list.owner and contest == achievement_list.contest):
            achievement_list.achievements.remove(achievement)
        return redirect('edit_achievement_list',contest.pk,achievement_list.pk)
    else:
        context  = {'contest':contest,
                    'achievement_list':achievement_list,
                    'achievement':achievement
                    }
        return render(request,'gamequest/edit_achievement_list_remove_achievement.html',context)


@login_required 
def achievementListAddAchievements(request,contest_id,achievement_list_id):
    """
    Allows a user to select and add an existing achievement to an achievement list
    """
    try:
        contest = Contest.objects.get(pk=contest_id)
    except Contest.DoesNotExist:
        raise Http404
    try: 
        achievement_list = AchievementList.objects.get(pk=achievement_list_id)
    except AchievementList.DoesNotExist: 
        raise HTTP404

    if request.method == 'POST':
        form = AddAchievementForm(request.POST)
        if form.is_valid() and contest.upcoming and achievement_list.owner == request.user:
            try:
                new_achievement = Achievement.objects.get(pk=form.cleaned_data['achievement']) 
            except Contest.DoesNotExist:
                raise Http404
            else:
                achievement_list.achievements.add(new_achievement) 
                achievement_list.save()
                return redirect('edit_achievement_list',contest_id,achievement_list_id)
    else:
        form = AddAchievementForm()

    context = {'contest':contest,
               'achievement_list':achievement_list,
                'form':form,}
    return render(request,'gamequest/edit_achievement_list_achievements.html',context)
