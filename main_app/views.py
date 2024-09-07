from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import JournalEntryForm
from .models import Trip, TripEvent



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
    tripevents_trip_doesnt_have = TripEvent.objects.exclude(id__in = trip.tripevents.all().values_list('id'))
    journalEntry_form = JournalEntryForm()
    return render(request, 'trips/detail.html', {
        'trip': trip,
        'journalEntry_form' :journalEntry_form,
        'tripevents': tripevents_trip_doesnt_have 
        })
@login_required
def add_journalEntry(request, trip_id):
    form = JournalEntryForm(request.POST)
    if form.is_valid():
        new_journalEntry = form.save(commit=False)
        new_journalEntry.trip_id = trip_id
        new_journalEntry.save()
    return redirect('trip-detail', trip_id=trip_id)

@login_required
def associate_tripevent(request, trip_id, tripevent_id):
    Trip.objects.get(id=trip_id).tripevents.add(tripevent_id)
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





