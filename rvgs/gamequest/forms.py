from django.forms import ModelForm 
from django.forms import Form 
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

class AddAchievementToListForm(Form):
    """
    Form presented to the user when adding achievements to an achievement list.
    """
    achievement = forms.ChoiceField(required=True)

    def __init__(self, *args, **kwargs):
        super(AddAchievementToListForm,self).__init__(*args,**kwargs)
        achievement_choices = [(achievement.id, unicode(achievement.game.name + "-" +achievement.name)) for achievement in Achievement.objects.all()]
        self.fields['achievement'].choices = achievement_choices

class AddAchievementForm(ModelForm):
    class Meta:
        model = Achievement
        feilds = ['game','name','description']
