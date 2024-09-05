from django.contrib import admin
from .models import Trip,JournalEntry, TripEvent

# Register your models here.
admin.site.register(Trip)
admin.site.register(JournalEntry)
admin.site.register(TripEvent)
