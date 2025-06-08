from django import forms

class PackageSearchForm(forms.Form):
    location = forms.CharField(required=False, label="Location", widget=forms.TextInput(attrs={'placeholder': 'Eg: Thailand'}))
    min_price = forms.DecimalField(required=False, label="Min Price", min_value=0)
    max_price = forms.DecimalField(required=False, label="Max Price", min_value=0)
    min_duration = forms.IntegerField(required=False, label="Min Days", min_value=1)

from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'booking_date', 'no_of_people']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }