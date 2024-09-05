from django import forms
from .models import JournalEntry

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['trip','description', 'start_date', 'end_date','destination', 'photo']
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
        