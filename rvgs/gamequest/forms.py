from django import forms
from django.forms import ModelForm

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
