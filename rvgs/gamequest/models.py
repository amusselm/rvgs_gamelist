from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class System(models.Model):
    """
    An object to represent a type of game platform. Keeps track of systems that
    emulate other systems. 
    """
    systemName = models.CharField(max_length=100)
    systemDescription = models.CharField(max_length=512)
    emulated = models.BooleanField(default=False)
    emulating = models.ForeignKey("System",blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
	return self.systemName


class Game(models.Model):
    """
    An object to represent a particular game title. Keeps track of all platforms
    that the game has been ported to.
    """
    name = models.CharField(max_length=100)
    ports = models.ManyToManyField(System)
    def __str__(self):
	return self.name

class Contest(models.Model):
    """
    An object to represent a 'contest', which is a collection of lists and a state
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=4096)
    upcoming = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    participants = models.ManyToManyField(User)
    def __str__(self):
	return self.name

class Achievement(models.Model):
    """
    An object to represent an achievement in game. Since games might have multiple 
    campaigns, it might be helpful to specify what we mean by completeion.
    """
    game = models.ForeignKey(Game,blank=False, null=False,on_delete=models.CASCADE ) 
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=4096)
    def __str__(self):
	return self.game.name + " - " + self.name
    

class Unlock(models.Model):
    """
    An object to represent when a user has completed a game. 
    """
    user = models.ForeignKey(User,blank=False, null=False,on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True) 
    achievement = models.ForeignKey(Achievement,blank=False,null=False,on_delete=models.CASCADE)
    contest = models.ManyToManyField(Contest)
    def __str__(self):
	return self.achievement.__str__() + " unlocked by " + self.user.username

class AchievementList(models.Model):
    """
    An object to represent a user's 'games list' that other users attempt complete
    for a specified contest
    """
    owner = models.ForeignKey(User,blank=False, null=False,on_delete=models.CASCADE)
    achievements = models.ManyToManyField(Achievement)
    contest = models.ForeignKey(Contest,blank=False,null=False,on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=4096)
    def __str__(self):
        return self.owner.username + "'s " + self.name + " list for " + self.contest.name


