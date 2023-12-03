from django import forms
from .models import CentralAC

class CentralACForm(forms.ModelForm):
    class Meta:
        model = CentralAC
        fields = ['centralAC_mode', 'centralAC_status', 'max_temperature', 'min_temperature', 'low_speed_fee', 'mid_speed_fee', 'high_speed_fee', 'default_target_temperature']