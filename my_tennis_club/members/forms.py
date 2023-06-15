from django import forms
from .models import Member, Item

class RecordForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['firstname', 'lastname', 'phone', 'joined_date']
class RecordITForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['typ', 'mark', 'size', 'color', 'wear', 'sex']
