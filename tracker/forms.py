from django import forms
from .models import Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'dosage', 'frequency']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Amoxicillin'}),
            'dosage': forms.TextInput(attrs={'placeholder': 'e.g., 500 mg or 2 tablets'}),
            'frequency': forms.TextInput(attrs={'placeholder': 'e.g., Twice daily or Every 8 hours'}),
        }