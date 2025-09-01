from user import models
from .models import Lost_reports
from django import forms

class LostReportForm(forms.ModelForm):
    class Meta:
        model = Lost_reports
        exclude = ['user', 'reported_at']
        fields = ['item_name', 'item_description', 'item_image', 'location', 'date_lost', 'contact']
