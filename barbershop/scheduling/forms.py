# forms.py is a file that contains the forms for the application
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Appointment

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }


