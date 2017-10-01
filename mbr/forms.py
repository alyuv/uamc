from django import forms
from mbr.models import FlightTable
from django.utils.translation import ugettext_lazy as _
import re
from datetime import datetime, timedelta


def single_index(index):
    if re.compile(r'\b[A-Z]{4}$').search(index):
        return index
    else:
        raise forms.ValidationError(_('Enter a valid index'), code='invalid')


def multi_index(indexes):
    incorrect_index = []
    temp_indexes = re.sub('\s+', ' ', indexes).split()
    for index in temp_indexes:
        try:
            single_index(index)
        except forms.ValidationError:
            incorrect_index.append(index)
    if incorrect_index:
        raise forms.ValidationError(_('Enter a valid index'), code='invalid')
    else:
        return ' '.join(temp_indexes)


class FlightTableForm(forms.ModelForm):
    class Meta:
        model = FlightTable
        exclude = ['airline']
        widgets = {
            'alt_airport': forms.Textarea(attrs={'cols': '23', 'rows': '2'}),
            'firs': forms.Textarea(attrs={'cols': '23', 'rows': '1'}),
        }

    def clean_flight_number(self):
        return single_index(self.cleaned_data.get('number')) #fill template after click on table

    def clean_airport_from(self):
        return single_index(self.cleaned_data.get('airport_from'))

    def clean_airport_to(self):
        return single_index(self.cleaned_data.get('airport_to'))

    def clean_alternative_airports(self):
        return multi_index(self.cleaned_data.get('alt_airport'))

    def clean_firs(self):
        return multi_index(self.cleaned_data.get('firs'))

    def clean(self):
        cleaned_data = super(FlightTableForm, self).clean()
        if not any([cleaned_data['region_c'], cleaned_data['region_g'],
                    cleaned_data['region_h'], cleaned_data['region_eur'],
                    cleaned_data['region_mid'], cleaned_data['region_sasia']]):
            self.add_error('region_c', _('Select one of the region'))

        if not any([cleaned_data['level450'], cleaned_data['level410'],
                    cleaned_data['level390'], cleaned_data['level360'],
                    cleaned_data['level340'], cleaned_data['level320'],
                    cleaned_data['level300'], cleaned_data['level270'],
                    cleaned_data['level240'], cleaned_data['level180'],
                    cleaned_data['level140'], cleaned_data['level100'],
                    cleaned_data['level050']]):
            self.add_error('fl450', _('Select one of the fly level'))

    def get_fly_level(self):
        fly_level = ['SH', 'SM']    # SH and SM always include in SIGWX
        for key in self.data:
            if key.startswith('level'):
                fly_level.append(key[5:])
        return fly_level

    def get_region(self):
        region = []
        for key in self.data:
            if key.startswith('region_'):
                region.append(key.split('_')[1].upper())
        return region

    def get_time(self):
        next_day = False
        now = datetime.utcnow()
        dt = datetime.strptime(self.data['departure_time'], '%H:%M').replace(
            year=now.year,
            month=now.month,
            day=now.day)
        if dt < datetime.utcnow():
            dt = dt + timedelta(days=1)
            next_day = True
        fd = datetime.strptime(self.data['flight_duration'], '%H:%M')
        at = dt + timedelta(hours=fd.hour, minutes=fd.minute)
        return next_day, {'departure_time': dt, 'arrival_time': at}
