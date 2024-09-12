import uuid
import boto3
import os
from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import JournalEntryForm
from django.shortcuts import get_object_or_404
from .models import Trip, TripEvent,Photo



# Create your views here.
class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

@login_required
def trip_index(request):
    trips = Trip.objects.filter(user=request.user) 
    return render(request, 'trips/index.html', {'trips': trips})

@login_required
def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    tripevents = TripEvent.objects.all()
    tripevents_trip_doesnt_have = TripEvent.objects.exclude(id__in = trip.tripevents.all().values_list('id'))
    journalEntry_form = JournalEntryForm()
    return render(request, 'trips/detail.html', {
        'trip': trip,
        'journalEntry_form' :journalEntry_form,
        'tripevents': tripevents_trip_doesnt_have           
         
        })

@login_required
def add_journalEntry(request, trip_id):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES)
        if form.is_valid():
            new_journalEntry = form.save(commit=False)
            new_journalEntry.trip_id = trip_id
            new_journalEntry.save()
            return redirect('trip-detail', trip_id=trip_id)
    else:
        form = JournalEntryForm()
    return render(request, 'trips/detail.html', {
        'form': form, 'trip_id': trip_id})

@login_required
def associate_tripevent(request, trip_id, tripevent_id):
    trip = get_object_or_404(Trip, id=trip_id)
    tripevent = get_object_or_404(TripEvent, id=tripevent_id)
    trip.tripevents.add(tripevent)
    return redirect('trip-detail', trip_id=trip_id)

@login_required
def remove_tripevent(request, trip_id, tripevent_id):
    trip = Trip.objects.get(id=trip_id)
    trip.tripevents.remove(tripevent_id)
    return redirect('trip-detail', trip_id=trip.id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('trip-index')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def some_function(request):
    secret_key = os.environ['SECRET_KEY']


def add_photo(request, trip_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, trip_id=trip_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('trip-detail', trip_id=trip_id)
  

class TripCreate(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['title', 'description', 'start_date', 'end_date', 'destination']
    # success_url = '/trips/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TripUpdate(LoginRequiredMixin,UpdateView):
    model = Trip
    fields = ['title', 'description', 'start_date', 'end_date', 'destination']


class TripDelete(LoginRequiredMixin,DeleteView):
    model = Trip
    success_url = '/trips/'

class TripEventCreate(LoginRequiredMixin,CreateView):
    model = TripEvent
    fields = '__all__'

class TripEventList(LoginRequiredMixin,ListView):
    model = TripEvent

class TripEventDetail(LoginRequiredMixin,DetailView):
    model = TripEvent

class TripEventUpdate(LoginRequiredMixin,UpdateView):
    model = TripEvent
    fields = ['trip', 'event_date','event']

class TripEventDelete(LoginRequiredMixin,DeleteView):
    model = TripEvent
    success_url = '/tripevents/'





