# forms.py
from django import forms
from miniaccounts.models import ProfileInfo

class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = ProfileInfo
        fields = ['bio', 'acc_type', 'country', 'gender', 'dob', 'email', 'phone', 'image']
