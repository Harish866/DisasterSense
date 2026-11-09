
from django import forms
from .models import Incident


class IncidentReportForm(forms.ModelForm):

    class Meta:
        model = Incident

        fields = [
            'title',
            'description',
            'incident_type',
            'location',
            'latitude',
            'longitude',
            'severity',
            'people_affected',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Severe flooding in residential area'
            }),

            'description': forms.Textarea(attrs={
                'placeholder': 'Describe what happened, people affected, '
                               'visible damage and immediate danger...',
                'rows': 5
            }),

            'location': forms.TextInput(attrs={
                'placeholder': 'e.g. Velachery, Chennai'
            }),

            'latitude': forms.NumberInput(attrs={
                'placeholder': 'e.g. 12.9750',
                'step': 'any'
            }),

            'longitude': forms.NumberInput(attrs={
                'placeholder': 'e.g. 80.2210',
                'step': 'any'
            }),

            'severity': forms.Select(
                choices=[
                    (1, '1 - Minor'),
                    (2, '2 - Moderate'),
                    (3, '3 - Serious'),
                    (4, '4 - Severe'),
                    (5, '5 - Extreme'),
                ]
            ),

            'people_affected': forms.NumberInput(attrs={
                'min': 0,
                'placeholder': 'Estimated number of people'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')

        if latitude is not None and not -90 <= latitude <= 90:
            self.add_error('latitude', 'Latitude must be between -90 and 90.')

        if longitude is not None and not -180 <= longitude <= 180:
            self.add_error('longitude', 'Longitude must be between -180 and 180.')

        return cleaned_data
