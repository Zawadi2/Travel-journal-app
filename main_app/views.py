from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import JournalEntryForm
from .models import Trip, TripEvent



# Create your views here.
def home(request):
    trips = Trip.objects.all()
    return render(request, 'home.html', {'trips': trips})

def about(request):
    return render(request, 'about.html')


def trip_index(request):
    trips = Trip.objects.all()
    return render(request, 'trips/index.html', {'trips': trips})


def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    tripevents_trip_doesnt_have = TripEvent.objects.exclude(id__in = trip.tripevents.all().values_list('id'))
    journalEntry_form = JournalEntryForm()
    return render(request, 'trips/detail.html', {
        'trip': trip,
        'journalEntry_form' :journalEntry_form,
        'tripevents': tripevents_trip_doesnt_have 
        })

def add_journalEntry(request, trip_id):
    form = JournalEntryForm(request.POST)
    if form.is_valid():
        new_journalEntry = form.save(commit=False)
        new_journalEntry.trip_id = trip_id
        new_journalEntry.save()
    return redirect('trip-detail', trip_id=trip_id)


class TripCreate(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['title', 'description', 'start_date', 'end_date', 'destination']
    success_url = '/trips/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TripUpdate(UpdateView):
    model = Trip
    fields = ['title', 'description', 'start_date', 'end_date', 'destination']

class TripDelete(DeleteView):
    model = Trip
    success_url = '/trips/'

class TripEventCreate(LoginRequiredMixin,CreateView):
    model = TripEvent
    fields = '__all__'

class TripEventList(ListView):
    model = TripEvent

class TripEventDetail(DetailView):
    model = TripEvent

class TripEventUpdate(UpdateView):
    model = TripEvent
    fields = ['trip', 'event_date','event']

class TripEventDelete(DeleteView):
    model = TripEvent
    success_url = '/tripevents/'





