from django import forms
from .models import Filter

class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['max_price', 'personal_bathroom', 'min_beds', 'min_bathrooms', 'move_in_date', 'length_of_stay', 'gender']
        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
        }
