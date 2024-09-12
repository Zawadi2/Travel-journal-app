from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



EVENTS = [
    ('S', 'Sightseeing'),
    ('E', 'Entertainment'),
    ('R', 'Relaxation'),
    ('A', 'Adventure'),
    ('H', 'Hiking'),
    ('W', 'Wedding'),
    ('M', 'Swimming'),
]
# # Create your models here.


class TripEvent(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    event_date = models.DateField('Event date')
    event= models.CharField(max_length=1,choices=EVENTS, default=EVENTS[0][0][0])
  
    def __str__(self):
        return f"{self.get_event_display()}  on {self.event_date}"
    
    def get_absolute_url(self):
        return reverse('tripevent-detail', kwargs={'pk': self.id})
    

    class Meta:
        ordering = ['-event_date']

class Trip(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField('Start date')
    end_date = models.DateField('End date')
    destination = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tripevents = models.ManyToManyField(TripEvent,related_name='trips')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('trip-detail', kwargs={'trip_id': self.id})
    
    
class JournalEntry(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField('JournalEntry date')
    end_date = models.DateField('JournalEntry date')
    destination = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    

    def __str__(self):
        return f"{self.get_trip_display()} on {self.destination}"
    
    class Meta:
        ordering = ['-start_date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for trip_id: {self.trip_id} @{self.url}"
