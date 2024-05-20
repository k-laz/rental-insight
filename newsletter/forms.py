from django import forms
from .models import User_Filter, Neighbourhood
from .widgets import RangeInput


class FilterForm(forms.ModelForm):
    min_beds = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Min', 'class': 'form-control', 'min': '0'}),
        min_value=0,  # Ensures the value is not negative on the server side
        required=False  # Adjust based on whether a value is required
    )
    max_beds = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Max', 'class': 'form-control', 'min': '0'}),
        min_value=0,  # Server-side validation for non-negative values
        required=False
    )
    min_baths = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Min', 'class': 'form-control', 'min': '0'}),
        min_value=0,  # Ensures the value is not negative on the server side
        required=False  # Adjust based on whether a value is required
    )
    max_baths = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Max', 'class': 'form-control', 'min': '0'}),
        min_value=0,  # Server-side validation for non-negative values
        required=False
    )

    class Meta:
        model = User_Filter
        fields = ['no_price_limit', 'price_limit', 'min_beds', 'max_beds', 'min_baths', 'max_baths', 'gender', 'personal_bathroom', 'full_place', 'furnished', 'neighbourhoods', 'move_in_date', 'length_of_stay']
        widgets = {
            'neighbourhoods': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'price_limit': RangeInput(attrs={'class': 'my-custom-class'}),
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
            'length_of_stay': forms.CheckboxSelectMultiple,
            'gender': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['price_limit'].label = 'Price Limit'
        self.fields['gender'].label = 'Gender Preference'
        self.fields['furnished'].label = 'Furnished'
        self.fields['full_place'].label = 'Full Place To Yourself'


    # TODO: not sure if this is the correct way to save no_price_limit if price is at max
    def save(self, commit=True):
        model_instance = super(FilterForm, self).save(commit=False)
        if self.cleaned_data['price_limit'] > 8000:
            self.fields['no_price_limit'] = True
        if commit:
            model_instance.save()

        return model_instance
    