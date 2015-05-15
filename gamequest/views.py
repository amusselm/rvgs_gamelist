from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import authenticate 

from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from models import *
from gamequest.forms import *

# Create your views here.
def index(request):
    return contestListView(request)

def contestListView(request):
    """
    Display all contests.
    """
    upcoming_contests = Contest.objects.filter(upcoming=True)
    active_contests = Contest.objects.filter(active=True)
    archive_contests = Contest.objects.filter(archive=True)
    context = {'upcoming':upcoming_contests,
       'active':active_contests,
       'archive':archive_contests,}
    return render(request, 'gamequest/contest_list.html', context)


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
        user_in_contest = False
        if request.user.is_authenticated():
            user_in_contest = contest.UserInContest(request.user)
        recent_unlocks = Unlock.objects.filter(contest__id = contest_id)
        recent_unlocks.order_by('timestamp')[:10]
        context = {'contest':contest,
                   'recent_unlocks':recent_unlocks,
                   'user_in_contest':user_in_contest,} 
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

@login_required 
def contestJoin(request,contest_id):
    """
    Adds the user to the given contest if called as an HTTP POST Request
    """
    try:
        contest = Contest.objects.get(pk=contest_id)
    except Contest.DoesNotExist:
        raise Http404
    else:
        if request.method == 'POST':
            if contest.upcoming or contest.active:
                contest.participants.add(request.user)
    return userProfileRedirect(request)
        

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
def achievementListRemove(request,contest_id,achievement_list_id):
    """
    Gives the user a confirmation page to remove a specific achievement from a list, or
    if it receives a POSt requrest, does the removal
    """
    #It's worth noting that this is very similar to removing an achievement from an
    # achievement list. As such, these functions should be refactored eventually
    try:
        contest = Contest.objects.get(pk=contest_id)
    except Contest.DoesNotExist:
        raise Http404
    try: 
        achievement_list = AchievementList.objects.get(pk=achievement_list_id)
    except AchievementList.DoesNotExist: 
        raise HTTP404
    if request.method == 'POST':
        if (request.user == achievement_list.owner and contest == achievement_list.contest):
            achievement_list.delete()
            return redirect('contest_participant',contest.pk,request.user.get_username())
    else:
        context  = {'contest':contest,
                    'achievement_list':achievement_list,
                    }
        return render(request,'gamequest/remove_achievement_list.html',context)




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
        form = AddAchievementToListForm(request.POST)
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
        form = AddAchievementToListForm()

    context = {'contest':contest,
               'achievement_list':achievement_list,
                'form':form,}
    return render(request,'gamequest/edit_achievement_list_achievements.html',context)

class AchievementListRefrenceBaseView(TemplateView):
    """A base class that's intended to be extended for any form that needs to refer
      back to a specific contest and achievement list """
    def get_contest(self):
        if(self.request.method == 'GET' ):
            from_contest = self.request.GET.get('from_contest')
        else:
            from_contest = self.request.POST.get('from_contest')
        return from_contest

    def get_list(self):
        if(self.request.method == 'GET' ):
            from_list = self.request.GET.get('from_list')
        else:
            from_list = self.request.POST.get('from_list')
        return from_list

    def get_context_data(self, **kwargs):
        context = super( AchievementListRefrenceBaseView, self).get_context_data(**kwargs)
        from_contest = self.get_contest() 
        from_list = self.get_list() 
        context['from_contest'] = from_contest
        context['from_list'] = from_list
        return context

class CreateSelectGameView(AchievementListRefrenceBaseView):
    """ 
    View class for handleing the add select game screen
    """
    template_name = 'gamequest/create_select_game.html'

    #These two 'constants' are used to for form prefixes
    # so that we can tell the difference between these forms when the user 
    # submits them
    CREATE_GAME_PREFIX = 'create_game'
    SELECT_GAME_PREFIX = 'select_game'

    def get(self, request):
        create_game_form = AddGameForm(prefix=self.CREATE_GAME_PREFIX)
        select_game_form = SelectGameForm(prefix=self.SELECT_GAME_PREFIX)
        from_contest = super(CreateSelectGameView,self).get_contest() 
        from_list = super(CreateSelectGameView,self).get_list() 
        context= { 
            'select_game_form' : select_game_form,
            'create_game_form' : create_game_form,
            'from_contest' : from_contest,
            'from_list' : from_list,
            'CREATE_GAME_PREFIX':self.CREATE_GAME_PREFIX,
            'SELECT_GAME_PREFIX':self.SELECT_GAME_PREFIX
        }

        return render (request, 'gamequest/create_select_game.html',context)

    def post(self, request):
        create_game_form= AddGameForm(prefix=self.CREATE_GAME_PREFIX)
        select_game_form = SelectGameForm(prefix=self.SELECT_GAME_PREFIX)
        success = False
    
        #Default to proscessing the create game form if we can't tell which 
        #form the user submitted
        action = self.request.POST.get('action',self.CREATE_GAME_PREFIX)

        if action==self.CREATE_GAME_PREFIX:
            create_game_form= AddGameForm(request.POST,prefix=self.CREATE_GAME_PREFIX)
            if create_game_form.is_valid():
                game = create_game_form.save()
                success = True
        elif action==self.SELECT_GAME_PREFIX:
            select_game_form = SelectGameForm(request.POST,prefix=self.SELECT_GAME_PREFIX)
            if select_game_form.is_valid():
                game = Game.objects.get(pk=select_game_form.cleaned_data['game']) 
                success = True
        else:
            raise ValueError

        from_contest = super(CreateSelectGameView,self).get_contest() 
        from_list = super(CreateSelectGameView,self).get_list() 
        if success: 
            # If the form is valid, we prosceed to the next page
            success_url = reverse('create_select_achievement',
                kwargs={'game_id':game.id} ) + \
                '?from_contest='+from_contest+ \
                '&from_list='+from_list
            return redirect(success_url)
        else:
            #... Otherwise, we re-render the page so the user can correct their error
            context= { 
                'select_game_form' : select_game_form,
                'create_game_form' : create_game_form,
                'from_contest' : from_contest,
                'from_list' : from_list,
                'CREATE_GAME_PREFIX':self.CREATE_GAME_PREFIX,
                'SELECT_GAME_PREFIX':self.SELECT_GAME_PREFIX
            }
            return render (request, 'gamequest/create_select_game.html',context)

class CreateSelectAchievementView(AchievementListRefrenceBaseView):
    """ 
    View class for handleing the add select achievement screen
    """
    template_name = 'gamequest/create_select_achievement.html'

    #These two 'constants' are used to for form prefixes
    # so that we can tell the difference between these forms when the user 
    # submits them
    CREATE_ACHIEVEMENT_PREFIX = 'create_achievement'
    SELECT_ACHIEVEMENT_PREFIX = 'select_achievement'

    def get(self, request, game_id):
        try:
            game=Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            raise Http404
        create_achievement_form = AddAchievementForm(prefix=self.CREATE_ACHIEVEMENT_PREFIX)
        select_achievement_form = SelectAchievementForm(game=game,prefix=self.SELECT_ACHIEVEMENT_PREFIX)
        from_contest = super(CreateSelectAchievementView,self).get_contest() 
        from_list = super(CreateSelectAchievementView,self).get_list() 
        context= { 
            'select_achievement_form' : select_achievement_form,
            'create_achievement_form' : create_achievement_form,
            'from_contest' : from_contest,
            'from_list' : from_list,
            'game' : game,
            'CREATE_ACHIEVEMENT_PREFIX':self.CREATE_ACHIEVEMENT_PREFIX,
            'SELECT_ACHIEVEMENT_PREFIX':self.SELECT_ACHIEVEMENT_PREFIX
        }

        return render (request,'gamequest/create_select_achievement.html',context)

    def post(self, request,game_id):
        try:
            game=Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            raise Http404
        create_achievement_form= AddAchievementForm(prefix=self.CREATE_ACHIEVEMENT_PREFIX)
        select_achievement_form = SelectAchievementForm(game=game,prefix=self.SELECT_ACHIEVEMENT_PREFIX)
        success = False
    
        #Default to proscessing the create achievement form if we can't tell which 
        #form the user submitted
        action = self.request.POST.get('action',self.CREATE_ACHIEVEMENT_PREFIX)

        if action==self.CREATE_ACHIEVEMENT_PREFIX:
            create_achievement_form= AddAchievementForm(request.POST,prefix=self.CREATE_ACHIEVEMENT_PREFIX)
            if create_achievement_form.is_valid():
                achievement = create_achievement_form.save(commit=False)
                achievement.game = game
                achievement.save()
                success = True
        elif action==self.SELECT_ACHIEVEMENT_PREFIX:
            select_achievement_form = SelectAchievementForm(request.POST,
                                                            prefix=self.SELECT_ACHIEVEMENT_PREFIX,
                                                            game=game);
            if select_achievement_form.is_valid():
                achievement = Achievement.objects.get(pk=select_achievement_form.cleaned_data['achievement']) 
                success = True
        else:
            raise ValueError

        from_contest = super(CreateSelectAchievementView,self).get_contest() 
        from_list = super(CreateSelectAchievementView,self).get_list() 
        if success: 
            #First, remember to acctually add it to the user's list
            self.add_to_user_list(achievement,from_list,request.user)
            # If the form is valid, we prosceed to the user's contest profile
            success_url = reverse('edit_achievement_list',kwargs=
                                      {'contest_id':from_contest,
                                      'achievement_list_id':from_list}
                                  )
            return redirect(success_url)
        else:
            #... Otherwise, we re-render the page so the user can correct their error
            context= { 
                'select_achievement_form' : select_achievement_form,
                'create_achievement_form' : create_achievement_form,
                'from_contest' : from_contest,
                'from_list' : from_list,
                'game' : game,
                'CREATE_ACHIEVEMENT_PREFIX':self.CREATE_ACHIEVEMENT_PREFIX,
                'SELECT_ACHIEVEMENT_PREFIX':self.SELECT_ACHIEVEMENT_PREFIX
            }
            return render (request, 'gamequest/create_select_achievement.html',context)
    
    def add_to_user_list(self,achievement,achievement_list_id,user):
        if user.is_authenticated():
            try:
                achievement_list = AchievementList.objects.get(pk=achievement_list_id) 
            except AchievementList.DoesNotExist:
                raise Http404

            #Users should only be able to add to a list when they own it
            if user != achievement_list.owner:
                raise PermissionDenied

            #Users should not be able to add items to their list once the contest has
            # started. 
            if not achievement_list.contest.upcoming:
                raise PermissionDenied
            
            achievement_list.achievements.add(achievement)


class AddAchievementView(AchievementListRefrenceBaseView):
    template_name = 'gamequest/add_achievement.html'
    form_class = AddAchievementForm

    def get_success_url(self):
        from_contest = super(AddAchievementView,self).get_contest() 
        from_list = super(AddAchievementView,self).get_list() 
        success_url = reverse('edit_achievement_list_add',
                              kwargs={'contest_id':from_contest,'achievement_list_id':from_list})
        return success_url

    def form_valid(self, form):
        form.save()
        return super(AddAchievementView,self).form_valid(form)
    

class CreateUserView(FormView):
    """
    Proscess a reqeust for a new user account
    """
    template_name = 'gamequest/create_user.html'
    form_class=NewUserForm
     
    def form_valid(self,form):
        """Called after all parts of the form are validated.
           In this instance, it does nearly all of the sanity checking in the 
           class"""
        new_user = form.save()
        user = authenticate(username=new_user.username,password=form.clean_password2())
        login(self.request,user)
        return userProfileRedirect(self.request) 
            

