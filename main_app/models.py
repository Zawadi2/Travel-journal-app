from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# # Create your models here.

class Trip(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField('Feeding date')
    end_date = models.DateField('Feeding date')
    destination = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('cat-detail', kwargs={'cat_id': self.id})
    
    
class JournalEntry(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    destination = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='trip_images')
    

    def __str__(self):
        return f"{self.title} - {self.destination}"

