from django.contrib import admin

from core.models import ListEntry, List, User

admin.site.register(List)
admin.site.register(ListEntry)
