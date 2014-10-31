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
    #`emulating = models.ForeignKey("System")


