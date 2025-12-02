from django import forms
from .models import Scheduling, Tutor

class SchedulingForm(forms.ModelForm):
    
    class Meta:
        model = Scheduling
        fields = [
            'tutor', 'pet', 'date_scheduling', 'services', 
            'status', 'percentage_discount', 'observations'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            field = self.fields.get(field_name)
            
            if isinstance(field.widget, forms.SelectMultiple):
                continue
                
            # Aplica form-select/form-control 
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
