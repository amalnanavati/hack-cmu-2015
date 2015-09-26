from django.contrib import admin

from .models import Event

# Register your models here.


class EventAdmin(admin.ModelAdmin):
    fields = ['who', 'when', 'where', 'what']

admin.site.register(Event, EventAdmin)
