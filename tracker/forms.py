from django import forms
from .models import Medicine
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'dosage', 'frequency']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Amoxicillin'}),
            'dosage': forms.TextInput(attrs={'placeholder': 'e.g., 500 mg or 2 tablets'}),
            'frequency': forms.TextInput(attrs={'placeholder': 'e.g., Twice daily or Every 8 hours'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required for receiving medicine email reminders.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)