# admin allows you to auto build a site to crud records, useful during testing?
from django.contrib import admin
from .models import Chamber, Player

admin.site.register(Chamber)
admin.site.register(Player)