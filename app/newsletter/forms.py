from django import forms
from .models import Filter, Neighbourhood

class FilterForm(forms.ModelForm):
    neighbourhoods = forms.ModelMultipleChoiceField(
        queryset=Neighbourhood.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False  # Adjust based on whether you require at least one selection
    )
        
    class Meta:
        model = Filter
        fields = ['max_price', 'personal_bathroom', 'min_beds', 'min_bathrooms', 'gender', 'furnished', 'neighbourhoods'] # 'move_in_date', 'length_of_stay',
