from django.forms.widgets import NumberInput

class RangeInput(NumberInput):
    input_type = 'range'

    def __init__(self, attrs=None):
        default_attrs = {'min': 0, 'max': 8100, 'step': 100}  
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)