from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView
from datetime import datetime, timedelta, timezone

from django.http import HttpResponse
from io import BytesIO
from .pdfprint import PdfPrint

from mbr.forms import FlightTableForm
from mbr.models import *
from mbr.warepdecoding import WarepMessage

from mbr.metartaf import MetarTaf
from mbr.metartafdecoder import MetarTafDecoder

from collections import OrderedDict

import json


class MeteoInfoMixin:
    def get_info(self, request_form):
        info = {'airports': [request_form.cleaned_data['airport_from'],
                             request_form.cleaned_data['airport_to']] +
                            request_form.cleaned_data['alt_airport'].split(),
                'fir_index': request_form.cleaned_data['firs'].split()}

        info['correct_airports'] = list(IcaoStation.objects.filter(
            station_index__in=(info['airports'])).values_list('station_index',
                                                              flat=True))
        info['correct_fir'] = list(IcaoStation.objects.filter(
            station_index__in=(info['fir_index'])).values_list('station_index',
                                                               flat=True))

        info['observation'] = self.get_observations(info['correct_airports'])
        info['forecast'] = self.get_forecast(info['correct_airports'])
        if info['correct_fir']:
            info['sigmets'] = self.get_sigmet(info['correct_fir'])
            info['aireps'] = self.get_airep(info['correct_fir'])
            if request_form.cleaned_data['airmet']:
                info['airmets'] = self.get_airmet(info['correct_fir'])
            if request_form.cleaned_data['gamet']:
                info['gamets'] = self.get_gamet(info['correct_fir'])

        info['fly_regions'] = request_form.get_region()
        info['fly_levels'] = request_form.get_fly_level()
        info['fly_levels'].sort()

        info['next_day'], info['time'] = request_form.get_time()

        info['wafc_charts'] = self.get_wafc_charts(info['fly_regions'],
                                                   info['fly_levels'],
                                                   info['time'])
        info['pyua98'] = self.get_PYUA98()
        info['qava91'] = self.get_QAVA91()
        info['phenomena_chart'] = self.get_MRL(level='H')
        info['heights_chart'] = self.get_MRL(level='J')
        info['volcanic_charts'] = self.get_VolcanicAshImg()
        info['request_data'] = self.get_RequestData(request_form)
        return info

    def get_observations(self, param):
        message = {}
        query = METAR.objects.filter(station__station_index__in=param) \
            .order_by('station', '-valid_end').distinct('station')

        def get_message_type(message: str):
            if message.startswith('SPECI'):
                return 'speci'
            else:
                return 'metar'

        for mes in query:
            ta_message_handle = MetarTaf(mes.message)
            ta_message = MetarTafDecoder(ta_message_handle)

            message[mes.station.station_index] = \
                dict(message=mes.message,
                     message_class=get_message_type(mes.message),
                     message_decoded=ta_message.string(),
                     id=mes.id)

        missing_index = set(param) - set(message.keys())
        for index in missing_index:
            message[index] = mbr_set_nil_message('METAR', index)
        return message

    def get_forecast(self, param):
        message = {}
        query = TAF.objects.filter(station__station_index__in=param,
                                   valid_end__gte=timezone.now()) \
            .order_by('station', '-channel_time', '-valid_end').distinct('station')

        for mes in query:
            taf_handle = MetarTaf(mes.message)
            taf_message = MetarTafDecoder(taf_handle)
            message[mes.station.station_index] = \
                dict(message=mes.message,
                     message_class='taf',
                     id=mes.id,
                     message_decoded=taf_message.string())

        missing_index = set(param) - set(message.keys())
        for index in missing_index:
            message[index] = mbr_set_nil_message('TAF', index)
        return message

    def get_sigmet(self, param):
        message = {}
        query = SIGMET.objects.filter(station__station_index__in=param,
                                      valid_end__gte=timezone.now()) \
            .order_by('station', '-valid_end').distinct('station')

        for mes in query:
            message.setdefault(mes.station.station_index, [])
            message[mes.station.station_index].append(
                dict(message=mes.message, message_class='sigmet', id=mes.id))

        missing_index = set(param) - set(message.keys())
        for index in missing_index:
            message[index] = [mbr_set_nil_message('SIGMET', index)]
        return message

    def get_airep(self, param):
        message = {}

        query = AIREP.objects.filter(station__station_index__in=param, valid_end__gte=timezone.now()-timedelta(days=1))\
            .order_by('station', '-valid_end')

        for mes in query:
            message.setdefault(mes.station.station_index, [])
            mssg = mes.gts_yygggg + " " + mes.message
            message[mes.station.station_index].append(
                dict(message=mssg, message_class='airep', id=mes.id))

        missing_index = set(param) - set(message.keys())
        for index in missing_index:
            message[index] = [mbr_set_nil_message('AIREP', index)]
        return message

    def get_airmet(self, param):
        message = {}

        query = AIRMET.objects.filter(station__station_index__in=param,
                                      valid_end__gte=timezone.now()) \
            .order_by('station', '-valid_end').distinct('station')

        for mes in query:
            message.setdefault(mes.station.station_index, [])
            message[mes.station.station_index].append(
                dict(message=mes.message, message_class='airmet', id=mes.id))

        missing_index = set(param) - set(message.keys())
        for index in missing_index:
            message[index] = [mbr_set_nil_message('AIRMET', index)]
        return message

    def get_gamet(self, param):
        message = {}

        query = GAMET.objects.filter(station__station_index__in=param, valid_end__gte=timezone.now()) \
            .order_by('station', '-valid_end', '-insert_time').distinct('station')

        for mes in query:
            message.setdefault(mes.station.station_index, [])
            message[mes.station.station_index].append(
                dict(message=mes.message, message_class='airmet', id=mes.id))

        missing_index = set(param) - set(message.keys())
        for index in missing_index:
            message[index] = [mbr_set_nil_message('GAMET', index)]
        return message

    def get_wafc_charts(self, region, level, time):
        wafc_charts = dict()

        departure_time = datetime.strptime(str(time['departure_time']) + '+0000', "%Y-%m-%d %H:%M:%S%z")
        arrival_time = datetime.strptime(str(time['arrival_time']) + '+0000', "%Y-%m-%d %H:%M:%S%z")

        grib = GRIB.objects.filter(region__in=region,
                                   valid_end__gte=departure_time,
                                   valid_begin__lte=arrival_time,
                                   im_level__in = level) \
                .values_list('id', 'valid_begin', 'valid_end', 'region',
                             'im_level', 'in_base64').order_by('-im_level', '-source_time', 'valid_begin')

        sigwx = SIGWX.objects.filter(region__in=region,
                                     valid_end__gte=departure_time,
                                     valid_begin__lte=arrival_time,
                                     im_level__in=level) \
            .values_list('id', 'valid_begin', 'valid_end', 'region',
                         'im_level', 'in_base64').order_by('-im_level', '-source_time', 'valid_begin')

        for map in (list(sigwx) + list(grib)):
            time = map[1] + (map[2] - map[1]) / 2
            wafc_charts.setdefault(time, {})
            wafc_charts[time].setdefault(map[3], {})  # region
            wafc_charts[time][map[3]].setdefault(map[4], {})  # FL
            wafc_charts[time][map[3]][map[4]].setdefault('id', map[0])
            wafc_charts[time][map[3]][map[4]].setdefault('base64', map[5])

        wafc_charts_sorted = OrderedDict(sorted(wafc_charts.items()))  # dict(sorted(wafc_charts.items()))
        return wafc_charts_sorted

    def get_PYUA98(self):
        return PYUA98.objects.filter(valid_end__gte=timezone.now()) \
            .order_by('-valid_end').values_list('id', flat=True).first()

    def get_QAVA91(self):
        return QAVA91.objects.filter(valid_end__gte=timezone.now()) \
            .order_by('-valid_end').values_list('id', flat=True).first()

    def get_MRL(self, level):
        return MRL.objects.filter(valid_end__gte=timezone.now(),
                                  im_level=level).order_by('-valid_end'). \
            values_list('id', 'in_base64').first()

    def get_VolcanicAshImg(self):
        return list(VolcanicAshImg.objects.filter(
            valid_end__gte=timezone.now()).order_by('-valid_end').
                    values_list('id', 'valid_begin', 'region'))

    def get_RequestData(self, request_form):
        request_data = dict(request_form.cleaned_data)
        keys = [key for key, value in request_data.items() if value == False]
        for key in keys:
            del request_data[key]
        return request_data


class FlightData(PermissionRequiredMixin, MeteoInfoMixin, FormView):
    form_class = FlightTableForm
    template_name = 'mbr/flightdata.html'
    permission_required = 'mbr.can_view_mbr_info'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        kwargs['request_form'] = FlightTableForm(request.POST)
        context = self.get_context_data(**kwargs)
        if '_handleshow' in request.POST:
            MbrLog(user=self.request.user, operation='Get data', request=context['request_data'],
                   result='result').save()
            return self.render_to_response(context)
        elif '_getpdf' in request.POST:
            response = HttpResponse(content_type='application/pdf')
            today = datetime.today()
            filename = '' + today.strftime('%Y-%m-%d %H-%M-%S')
            response['Content-Disposition'] = 'inline; filename={0}.pdf'.format(filename)  # for show
            buffer = BytesIO()
            report = PdfPrint(buffer, filename, context, 'A4')
            pdf = report.report('Flight Information')
            MbrLog(user=self.request.user, operation='Get PDF', request=context['request_data'],
                   result='result').save()
            response.write(pdf)
            return response

    def get_context_data(self, **kwargs):
        context = super(FlightData, self).get_context_data(**kwargs)

        if 'request_form' in kwargs:
            if kwargs['request_form'].is_valid():
                context.update(self.get_info(kwargs['request_form']))
                # VIEW or PDF
            context['form'] = kwargs['request_form']

            request = render(self.request,
                             'mbr/mbr_set_log_request.html',
                             context={'data': context['form']}).content.decode("utf-8").strip()

            view_request = 'from ' + context['form']['airport_from'].data + ', to ' + context['form']['airport_to'].data

            result = render(self.request,
                            'mbr/mbr_set_log_result_view.html',
                            context={'result': 'Just example '}).content.decode("utf-8").strip()

        else:
            context['form'] = FlightTableForm()

        context['flight_list'] = FlightTable.objects.filter(
            airline=Airline.objects.filter(
                auth_group__in=self.request.user.groups.all()))
        context['flight_data'] = flight_data(context['flight_list'])
        return context


class ListMRL(LoginRequiredMixin, ListView):
    level = 'J'
    model = MRL
    template_name = 'mbr/mrl_animation.html'
    paginate_by = 5
    context_object_name = 'scans'

    def get_queryset(self):
        queryset = self.model.objects.filter(im_level=self.level)
        return queryset


class Warep(LoginRequiredMixin, ListView):
    model = WAREP
    template_name = 'mbr/warep.html'
    context_object_name = 'wareplist'

    def generateGeoJson(self, warep):
        warepmessage = WarepMessage(warep.message, warep.station.name_en, datetime.utcnow())
        warepmessage.decode()
        geoJsonWarep = {
            "type": "Feature",
            "properties": {
                "station_index": str(warep.station.station_index),
                "name_en": warep.station.name_en,
                "name_ua": warep.station.name_uk,
                "name_ru": warep.station.name_ru,
                "channel": warep.channel,
                "gts_yygggg": warep.gts_yygggg,
                "gts_bbb": warep.gts_bbb,
                "insert_time": warep.insert_time.strftime('%d.%m.%y %H:%M'),
                "channel_time": warep.channel_time.strftime('%d.%m.%y %H:%M'),
                "valid_begin": warep.valid_begin.strftime('%d.%m.%y %H:%M'),
                "valid_end": warep.valid_end.strftime('%d.%m.%y %H:%M'),
                "message": warep.message,
                "fir": warep.station.fir,
                "popupContent": warepmessage.generatePopupContent()
            },
            "geometry": {
                "type": "Point",
                "coordinates": [str(warep.station.lon), str(warep.station.lat)]
            },
            "id": str(warep.station.station_index)
        }

        return geoJsonWarep

    def get_queryset(self):
        geoJsonWareps = dict()
        geoJsonStormWareps = {
            "type": "FeatureCollection",
            "metadata": {
                "generated": "",
                "url": "namc.com.ua",
                "title": "Ukraine Actuals Storm Wareps",
            },
            "features": []
        }
        geoJsonAviaWareps = {
            "type": "FeatureCollection",
            "metadata": {
                "generated": "",
                "url": "namc.com.ua",
                "title": "Ukraine Actuals Avia Wareps",
            },
            "features": []
        }
        queryset = WAREP.objects.select_related('station').filter(valid_end__gte=timezone.now()).order_by('-valid_end')

        for warep in queryset:
            jsonWarep = self.generateGeoJson(warep)
            if warep.message.find('STORM') > -1:
                geoJsonStormWareps['features'].append(jsonWarep)
            elif warep.message.find('AVIA') > -1:
                geoJsonAviaWareps['features'].append(jsonWarep)
            geoJsonWareps = {'storm': json.dumps(geoJsonStormWareps), 'avia': json.dumps(geoJsonAviaWareps)}
        return geoJsonWareps


class FlightList(ListView):
    context_object_name = 'fligts_list'
    model = FlightTable
    template_name = 'mbr/flight/list.html'

    # context_object_name

    def get_queryset(self):
        queryset = self.model.objects.filter(
            airline__auth_group=self.request.user.groups.
                filter(name__startswith='AL'))
        return queryset


class AddFlight(CreateView):
    form_class = FlightTableForm
    template_name = 'mbr/flight/create_flight.html'

    def get_success_url(self):
        return reverse('flight_list')

    def form_valid(self, form):
        airline = Airline.objects.filter(
            auth_group=self.request.user.groups.filter(name__startswith='AL')
            [0]).get()
        form.instance.airline = airline
        form.save()
        return super(AddFlight, self).form_valid(form)


class UpdateFlight(UpdateView):
    form_class = FlightTableForm
    model = FlightTable
    template_name = 'mbr/flight/update_flight.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateFlight, self).get_context_data(**kwargs)
        context['key'] = self.get_object().id
        context['action'] = reverse('mbr_update_flight',
                                    kwargs={'pk': self.get_object().id})
        return context

    def get_success_url(self):
        return reverse('flight_list')


class DeleteFlight(DeleteView):
    model = FlightTableForm
    template_name = 'mbr/flight/delete_flight.html'

    def get_success_url(self):
        return reverse('flight_list')


class ViewBaseMap(DetailView):
    context_object_name = 'map'
    model = BaseMap
    template_name = 'mbr/info/view_map.html'


class ViewGRIB(ViewBaseMap):
    model = GRIB


class ViewSIGWX(ViewBaseMap):
    model = SIGWX


class ViewMRL(ViewBaseMap):
    model = MRL


class ViewPYUA98(ViewBaseMap):
    model = PYUA98


class ViewQAVA91(ViewBaseMap):
    model = QAVA91


class ViewVolcanicAshImg(ViewBaseMap):
    model = VolcanicAshImg


class ViewMbrLog(ListView):
    context_object_name = 'log_request_list'
    model = MbrLog
    template_name = 'mbr/mbr_set_log_request.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user).order_by('-actiondate')
        return queryset
        # auth_user user.id


def flight_data(flight_list):
    flight_info = dict()
    for flight in flight_list:
        flight_info[flight.id] = \
            dict(number=flight.number,
                 airport_from=flight.airport_from,
                 airport_to=flight.airport_to,
                 alt_airport=flight.alt_airport,
                 departure_time=flight.departure_time.strftime("%H:%M"),
                 flight_duration=flight.flight_duration.strftime("%H:%M"),
                 firs=flight.firs,
                 level450=flight.level450,
                 level410=flight.level410,
                 level390=flight.level390,
                 level360=flight.level360,
                 level340=flight.level340,
                 level320=flight.level320,
                 level300=flight.level300,
                 level270=flight.level270,
                 level240=flight.level240,
                 level180=flight.level180,
                 level100=flight.level100,
                 level050=flight.level050,
                 region_c=flight.region_c,
                 region_g=flight.region_g,
                 region_h=flight.region_h,
                 region_eur=flight.region_eur,
                 region_mid=flight.region_mid,
                 region_sasia=flight.region_sasia,

                 airmet=flight.airmet, gamet=flight.gamet,
                 volcanic_ash=flight.volcanic_ash)
    return json.dumps(flight_info)


def mbr_set_nil_message(type_message, index):
    return dict(message='{} {} NIL='.format(type_message, index),
                message_class='nil', id=None)
