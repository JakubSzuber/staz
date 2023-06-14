from django import forms
from .models import Member

class RecordForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['firstname', 'lastname', 'phone', 'joined_date']
