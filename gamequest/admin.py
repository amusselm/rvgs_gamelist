from django.contrib import admin

from gamequest.models import *


# Register your models here.
admin.site.register(System)
admin.site.register(Game)
admin.site.register(Contest)
admin.site.register(Achievement)
admin.site.register(Unlock)
admin.site.register(AchievementList)

