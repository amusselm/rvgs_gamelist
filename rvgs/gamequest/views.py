from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader

from models import System, Game

# Create your views here.
def index(request):
    return HttpResponse("Index!")

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
    except System.DoesNotExist:
	raise Http404
    else:
	context = {'game':game,}
	return render(request,'gamequest/game.html',context)

