from django import forms
from django.forms import extras

class CalendarForm(forms.Form):
    calender_date = forms.DateField(
                            widget=extras.SelectDateWidget(
                                                        empty_label="Nothing"))
