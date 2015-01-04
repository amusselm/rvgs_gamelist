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

class AddAchievementForm(Form):
    """
    Form presented to the user when adding achievements to an achievement list.
    """
    game = forms.ChoiceField(required=False)
    achievement = forms.ChoiceField(required=True)
