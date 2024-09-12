from django.contrib import admin
from .models import Trip,JournalEntry, TripEvent, Photo

# Register your models here.
admin.site.register(Trip)
admin.site.register(JournalEntry)
admin.site.register(TripEvent)
admin.site.register(Photo)
