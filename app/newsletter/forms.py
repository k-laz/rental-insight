from django import forms
from .models import Filter, Neighbourhood

class FilterForm(forms.ModelForm):
    neighbourhoods = forms.ModelMultipleChoiceField(
        queryset=Neighbourhood.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False  # Adjust based on whether you require at least one selection
    )

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['min_beds'].label = 'Beds+'
        self.fields['min_bathrooms'].label = 'Baths+'
        self.fields['gender'].label = 'Gender Preference'
        self.fields['furnished'].label = 'Furnished'
        self.fields['full_place'].label = 'Full Place To Yourself'
        
    class Meta:
        model = Filter
        fields = ['max_price', 'min_beds', 'min_bathrooms', 'gender', 'personal_bathroom', 'full_place', 'furnished', 'neighbourhoods'] # 'move_in_date', 'length_of_stay',
