from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('trips/', views.trip_index, name='trip-index'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip-detail'),
    path('trips/create/', views.TripCreate.as_view(), name='trip-create'),
    path('trips/<int:pk>/update/', views.TripUpdate.as_view(), name='trip-update'),
    path('trips/<int:pk>/delete/', views.TripDelete.as_view(), name='trip-delete'), 
    path('trips/<int:trip_id>/add-journalEntry/', views.add_journalEntry, name='add-journalEntry'),
    path('tripevents/create/', views.TripEventCreate.as_view(), name='tripevent-create'),
    path('tripevents/<int:pk>/', views.TripEventDetail.as_view(), name='tripevent-detail'),
    path('tripevents/', views.TripEventList.as_view(), name='tripevent-index'),
    path('tripevents/<int:pk>/update/', views.TripEventUpdate.as_view(), name='tripevent-update'),
    path('tripevents/<int:pk>/delete/', views.TripEventDelete.as_view(), name='tripevent-delete'),

]
