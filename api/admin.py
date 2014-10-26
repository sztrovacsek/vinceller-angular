from django.contrib import admin
from .models import *

class WineAdmin(admin.ModelAdmin):
    pass

admin.site.register(Wine, WineAdmin)
