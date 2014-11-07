from django.db import models

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
