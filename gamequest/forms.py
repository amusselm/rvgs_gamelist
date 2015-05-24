from django.forms import ModelForm 
from django.forms import Form 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 

from gamequest.models import *

class AchievementListForm(ModelForm):
    """
    Form presented to the user when creating and editing an achievement list. Note that
    this form only allows the user to edit and change the name and description, not 
    the contents of the list.
    """
    class Meta:
        model = AchievementList
        fields = ['name','description']

class SelectAchievementForm(Form):
    """
    Form presented to the user when adding achievements to an achievement list.
    """
    achievement = forms.ChoiceField(required=True)

    def __init__(self,  *args, **kwargs):
        game = kwargs.pop('game',None)
        super(SelectAchievementForm,self).__init__(*args,**kwargs)
        achievement_choices = [
            (achievement.id, unicode(achievement.name))  
            for achievement in Achievement.objects.filter(game__id=game.id)
        ]
        self.fields['achievement'].choices = achievement_choices

class AddAchievementForm(ModelForm):
    """
    Form to add a new achievement to the system
    """
    class Meta:
        model = Achievement
        fields = ['name','description']

class SelectGameForm(Form):
    """
    Form to select an existing game from a list
    """
    game = forms.ChoiceField(required=True)

    def __init__(self, *args, **kwargs):
        super(SelectGameForm,self).__init__(*args,**kwargs)
        game_choices = [(game.id, unicode(game.name)) \
            for game in Game.objects.all().order_by('name')]
        self.fields['game'].choices = game_choices



class AddGameForm(ModelForm):
    """
    Form to add a new game to the system
    """
    class Meta:
        model = Game
        fields = ['name','ports','description']

    def __init__(self, *args, **kwargs):
        super(AddGameForm,self).__init__(*args,**kwargs)
        platforms = [(platform.id, unicode(platform.systemName)) for platform in System.objects.filter(emulated=False)]
        self.fields['ports'].choices = platforms
        
class NewUserForm(UserCreationForm):
    """
    For to allow new users to register
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ( "username", "email")
        
