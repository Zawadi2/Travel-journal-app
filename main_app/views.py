from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Trip



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
    return render(request, 'trips/detail.html', {'trip': trip})



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




