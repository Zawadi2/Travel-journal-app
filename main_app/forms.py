from django import forms
from .models import JournalEntry
from .models import TripEvent

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['trip','description', 'start_date', 'end_date','destination',]
        widgets = {
            'start_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),

        'end_date': forms.DateInput(
        format=('%Y-%m-%d'),
        attrs={
            'placeholder': 'Select an end date',
            'type': 'date'
        }
    ),
}
        
class TripEventForm(forms.ModelForm):
    class Meta:
        model = TripEvent
        fields = ['trip', 'event_date', 'event']

        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }

       