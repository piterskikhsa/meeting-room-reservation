from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from meeting_room_reservation.models import ReservedMeetingTime, MeetingRoom


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2',)


class MyForm(forms.ModelForm):

    class Meta:
        model = ReservedMeetingTime
        fields = ('start_meeting_time', 'end_meeting_time', 'title')
        widgets = {
            'start_meeting_time': forms.DateInput(attrs={'id': 'startimepicker'}),
            'end_meeting_time': forms.DateInput(attrs={'id': 'endtimepicker'}),
        }
