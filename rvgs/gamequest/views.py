from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader

from models import System

def index(request):
    return HttpResponse("Index!")

# Create your views here.
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

