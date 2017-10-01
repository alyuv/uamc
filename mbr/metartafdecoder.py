from django.utils.translation import gettext as _
from mbr.datatypes import *

REPORT_TYPE = {"METAR": _('METAR'), "SPECIAL": _('SPECIAL'), "TAF": _('TAF'),
               "COR": _('COR'), "AMD": _('AMD'), 'RTD': _('RTD'), 'AUTO': _('AUTO')}

DIRECTIONS = {'N': _('NORTHWARD'), 'E': _('ESTERLY'), 'S': _('SOUTHERLY'), 'W': _('WESTERLY'), 'NE': _('NORTHEASTERLY'),
              'SE': _('SOUTHEASTERLY'), 'SW': _('SOUTHWESTERLY'), 'NW': _('NORTHWESTERLY')}

loc_terms = [("OHD", "overhead"),
             ("DSNT", "distant"),
             ("AND", "and"),
             ("VC", "nearby")]


def xlate_loc(loc):
    for code, english in loc_terms:
        loc = loc.replace(code, english)
    return loc


## translation of the sky-condition codes into
TYPE_FORECAST ={"NOSIG": _("")}

SKY_COVER = {"SKC": _("CLEAR"),
             "CLR": _("CLEAR"),
             "NSC": _("NO_SIGNIFICANT_CLOUDS"),
             "NCD": _("AUTO_MONITOR_SYSTEM_DOES_NOT_DETECT_CLOUDS"),
             "FEW": _("A_FEW"),
             "SCT": _("SCATTERED"),
             "BKN": _("BROKEN"),
             "OVC": _("OVERCAST"),
             "///": "",
             "VV": _("INDEFINITE_CEILING")}

CLOUD_TYPE = {"TCU": _("TOWERING_CUMULUS"),
              "CU": _("CUMULUS"),
              "CB": _("CUMULONIMBUS"),
              "SC": _("STRATOCUMULUS"),
              "CBMAM": _("CUMULONIMBUS_MAMMATUS"),
              "ACC": _("ALTOCUMULUS_CASTELLANUS"),
              "SCSL": _("STANDING_LENTICULAR_STRATOCUMULUS"),
              "CCSL": _("STANDING_LENTICULAR_CIRROCUMULUS"),
              "ACSL": _("STANDING_LENTICULAR_ALTOCUMULUS")}

## translation of the present-weather codes

WEATHER_INT = {"-": _("LIGHT"),
               "+": _("HEAVY"),
               "-VC": _("NEARBY_LIGHT"),
               "+VC": _("NEARBY_HEAVY"),
               "VC": _("NEARBY")}

WEATHER_DESC = {"MI": _("SHALLOW"),
                "PR": _("PARTIAL"),
                "BC": _("PATCHES_OF"),
                "DR": _("LOW_DRIFTING"),
                "BL": _("BLOWING"),
                "SH": _("SHOWERS"),
                "TS": _("THUNDERSTORM"),
                "FZ": _("FREEZING")}

WEATHER_PREC = {"DZ": _("DRIZZLE"),
                "RA": _("RAIN"),
                "SN": _("SNOW"),
                "SG": _("SNOW_GRAINS"),
                "IC": _("ICE_CRYSTALS"),
                "PL": _("ICE_PELLETS"),
                "GR": _("HAIL"),
                "GS": _("SNOW_PELLETS"),
                "UP": _("UNKNOWN_PRECIPITATION"),
                "//": ""}

WEATHER_OBSC = {"BR": _("MIST"),
                "FG": _("FOG"),
                "FU": _("SMOKE"),
                "VA": _("VOLCANIC_ASH"),
                "DU": _("DUST"),
                "SA": _("SAND"),
                "HZ": _("HAZE"),
                "PY": _("SPRAY")}

WEATHER_OTHER = {"PO": _("SAND_WHIRLS"),
                 "SQ": _("SQUALLS"),
                 "FC": _("FUNNEL_CLOUD"),
                 "SS": _("SANDSTORM"),
                 "DS": _("DUST_STORM"),
                 "NSW": _("NO_SIGNIFICANT_WEATHER"),
                 "NSC": _("NO_SIGNIFICANT_CLOUDS")}

WEATHER_SPECIAL = {"+FC": _("TORNADO")}

COLOR = {"BLU": "blue",
         "GRN": "green",
         "WHT": "white"}

## translation of the runway
RUNWAY = {"88": _("ALL_RUNWAY"),
          "99": _("STATE_REPORT_IS_NOT_AVAILABLE"),
          "R": _("RIGHT"),
          "C": _("CENTRAL"),
          "L": _("LEFT")}

DEPOSIT_TYPE = {'0': _('CLEAR_AND_DRY'),
                '1': _('DAMP'),
                '2': _('WET_AND_WATER_PATCHES'),
                '3': _('RIME_AND_FROST_COVERED'),
                '4': _('DRY_SNOW'),
                '5': _('WET_SNOW'),
                '6': _('SLUSH'),
                '7': _('ICE'),
                '8': _('COMPACTED_OR_ROLLED_SNOW'),
                '9': _('FROZEN_RUTS_OR_RIDGES'),
                '/': _('TYPE_OF_DEPOSIT_NOT_REPORTED')
                }

EXTENT_TYPE = {'1': _('PERCENT_OF_RUNWAY_LESS_THAN'),
               '2': _('PERCENT_OF_RUNWAY').format('11 - 25'),
               '5': _('PERCENT_OF_RUNWAY').format('26 - 50'),
               '9': _('PERCENT_OF_RUNWAY').format('51 - 100'),
               '/': _('EXTENT_CONTAMINATION_NOT_REPORTED')}

DEPTH_TYPE = {'00': _('DEPTH_LESS_THAN_1_MM'),
              '92': _('DEPTH_CM').format('10'),
              '93': _('DEPTH_CM').format('15'),
              '94': _('DEPTH_CM').format('20'),
              '95': _('DEPTH_CM').format('25'),
              '96': _('DEPTH_CM').format('30'),
              '97': _('DEPTH_CM').format('35'),
              '98': _('DEPTH_CM_40'),
              '99': _('CLOSED_DUE_TO_SNOW'),
              '//': _('DEPTH_NOT_MEASURABLE'),
              }

FRICTION_TYPE = {'91': _('FRICTION_POOR'),
                 '92': _('FRICTION_MEDIUM_POOR'),
                 '93': _('FRICTION_MEDIUM'),
                 '94': _('FRICTION_MEDIUM_GOOD'),
                 '95': _('FRICTION_GOOD'),
                 '99': _('UNRELIABLE_INFO_FRICTION'),
                 '//': _('FRICTION_NOT_REPORTED')}

"""
RUNWAY = {"88": _("ALL_RUNWAY"),
          "99": _("STATE_REPORT_IS_NOT_AVAILABLE"),
          "R": _("RIGHT"),
          "C": _("CENTRAL"),
          "L": _("LEFT"),
          "P": _("MORE_THAN"),
          "M": _("LESS_THAN"),
          "V": "-",
          "U": _("INCREASING"),
          "D": _("DECREASING"),
          "N": _("NO_CHANGE"),
          "RWY": _("ON_RANWAY"),
          "ALLRWY": _("ALL_RUNWAY")}
"""
RUNWAY_STATE = {}

MISSING_RE = re.compile(r"^[M/]+$")


## Exceptions
class DecodeError(Exception):
    """Exception raised when an unparseable group is found in body of the report."""
    pass


## METARTAF decoder report objects
debug = False


class MetarTafDecoder(object):
    def __init__(self, metartaf):

        self.mt = metartaf

    def __str__(self):
        pass

    def _decodeType(self):

        type_report = ''
        if self.mt.type == None:
            type_report = _('UNKNOWN_TYPE')
        elif self.mt.type in REPORT_TYPE:
            type_report = REPORT_TYPE[self.mt.type]
        else:
            type_report = self.mt.type + " report"
        if self.mt.mod:
            if self.mt.mod in REPORT_TYPE:
                type_report += REPORT_TYPE[self.mt.mod]
            else:
                type_report += self.mt.mod
        if debug: print(type_report)
        return type_report

    def _decodeTypeForecast(self, d):

        text =""
        if d == 'NOSIG':
            text = _('NO_SIGNIFICANT_CHANGES')
        if d == 'TEMPO':
            text = _('TEMPORARY')
        if d == 'BECMG':
            text = _('BECOMING')
        if d == 'PROB30':
            text = _('PROB30') + ' '
        if d == 'PROB40':
            text = _('PROB40') + ' '
        if debug: print(text)
        return text

    def _decodeIndexAirport(self, d):
        aerodrome = " " + d
        if debug: print(aerodrome)
        return aerodrome

    def _decodeNil(self, d):
        if debug: print(_("NIL"))
        return _("NIL")

    def _decodeDateTime(self, d):
        dt = _('FOR_UTC').format(d['hour'], d['min'], d['day'])
        if debug: print(dt)
        return dt

    def _decodeForecastDateTime(self, d):
        forecastperiod = _('BETWEEN_UTC_AND_UTC').format(d['from_day'], d['from_hour'], d['till_day'],
                                                         d['till_hour'])
        if debug: print(forecastperiod)
        return forecastperiod

    def _decodeWind(self, d):
        wind_gust = None
        wind_dir_from = None
        wind_dir_to = None

        wind_dir = d['dir'].replace('O', '0')
        if wind_dir != "VRB" and wind_dir != "///" and wind_dir != "MMM":
            wind_dir = direction(wind_dir)
        wind_speed = d['speed'].replace('O', '0')
        units = d['units']
        if units == 'KTS' or units == 'K' or units == 'T' or units == 'LT':
            units = 'KT'
        if wind_speed.startswith("P"):
            wind_speed = speed(wind_speed[1:], units, ">")
        elif not MISSING_RE.match(wind_speed):
            wind_speed = speed(wind_speed, units)
        if d['gust']:
            wind_gust = d['gust']
            if wind_gust.startswith("P"):
                wind_gust = speed(wind_gust[1:], units, ">")
            elif not MISSING_RE.match(wind_gust):
                wind_gust = speed(wind_gust, units)
        if d['varfrom']:
            wind_dir_from = direction(d['varfrom'])
            wind_dir_to = direction(d['varto'])
        """
              Return a textual description of the wind conditions.
            Units may be specified as "MPS", "KT", "KMH", or "MPH".
        """
        text = _("WIND")
        if wind_speed == None or wind_speed == '//':
            text += " " + _("MISSING")
            return text
        elif wind_speed.value() == 0.0:
            text += " " + _("CALM")
        else:
            wind_speed = wind_speed.string(units)
            if not wind_dir or wind_dir == 'VRB':
                text += " " + _("VARIABLE").format(wind_speed)
            elif wind_dir_from:
                text += " " + _("VARIATIONS").format(wind_dir_from.string(), wind_dir_to.string(), wind_speed)
            else:
                text += " " + _("WIND_DIRECT_SPEED").format(wind_dir.string(), wind_speed)

            if wind_gust:
                text += _("GUSTING").format(wind_gust.string(units))
        if debug: print(text)
        return text

    def _decodeVisibility(self, d, min=None, units=None):
        cavok = d['vis']
        vis = d['dist']
        vis_less = None
        vis_dir = None
        vis_units = "M"
        vis_dist = "10000"
        if d['dist'] and d['dist'] != '////':
            vis_dist = d['dist']
            if d['dir'] and d['dir'] != 'NDV':
                vis_dir = d['dir']
        elif d['distu']:
            vis_dist = d['distu']
            if d['units'] and d['units'] != "U":
                vis_units = d['units']
        if vis_dist == "9999":
            vis_dist = "10000"
            vis_less = ">"
        if vis:
            if min == 'min':
                text = _("MIN_VISIBILITY")
            else:
                text = _("VISIBILITY")

            vis = distance(vis_dist, vis_units, vis_less)
            if vis_dir:
                vis_dir = direction(vis_dir)
                text += " " + _("VISIBILITY_AND_DIR").format(vis.string(units), vis_dir.compass_str())
            else:
                text += " %s" % (vis.string(units))
        elif cavok == 'CAVOK':
            text = _("CAVOK")

        if debug: print(text)
        return text

    def _decodeRunwayVisibility(self, d, units=None):
        lines = []
        for name, rvr_low, rvr_high in d:
            low = distance(rvr_low)
            high = distance(rvr_high)
            if rvr_low != rvr_high:
                lines.append(_('RUNWAY_VISIBILITY_RANGE').format(name, low.string(units), high.string(units)))
            else:
                lines.append(_('RUNWAY_VISIBILITY').format(name, low.string(units)))
        if debug: print("; ".join(lines))
        return "; ".join(lines)

    def _decodePresentWeather(self, d):
        text_list = []
        text_list.append(_("PRESENT_WEATHER"))
        for weatheri in d:
            (inteni, desci, preci, obsci, otheri) = weatheri
            text_parts = []
            code_parts = []
            if inteni:
                code_parts.append(inteni)
                text_parts.append(WEATHER_INT[inteni])
            if desci:
                code_parts.append(desci)
                if desci != "SH" or not preci:
                    text_parts.append(WEATHER_DESC[desci[0:2]])
                    if len(desci) == 4:
                        text_parts.append(WEATHER_DESC[desci[2:]])
            if preci:
                code_parts.append(preci)
                if len(preci) == 2:
                    precip_text = WEATHER_PREC[preci]
                elif len(preci) == 4:
                    precip_text = WEATHER_PREC[preci[:2]] + _("AND")
                    precip_text += WEATHER_PREC[preci[2:]]
                elif len(preci) == 6:
                    precip_text = WEATHER_PREC[preci[:2]] + ", "
                    precip_text += WEATHER_PREC[preci[2:4]] + _("AND")
                    precip_text += WEATHER_PREC[preci[4:]]
                if desci == "TS":
                    text_parts.append(_("WITH"))
                text_parts.append(precip_text)
                if desci == "SH":
                    text_parts.append(WEATHER_DESC[desci])
            if obsci:
                code_parts.append(obsci)
                text_parts.append(WEATHER_OBSC[obsci])

            if otheri:
                code_parts.append(otheri)
                text_parts.append(WEATHER_OTHER[otheri])
            code = " ".join(code_parts)
            if code in WEATHER_SPECIAL:
                text_list.append(WEATHER_SPECIAL[code])
            else:
                text_list.append(" ".join(text_parts))
        if debug: print("; ".join(text_list))
        return "; ".join(text_list).replace(';', ':', 1)

    def _decodeSkyConditions(self, d, sep="; "):
        text_list = []
        text_list.append(_("CLOUDS"))
        for skyi in d:
            (cover, height, cloud) = skyi
            if height:
                _height = distance(int(height) * 30, "M")  # meters
            if cover == "SKC" or cover == "CLR" or cover == "NSC" or cover == "NCD":
                text_list.append(SKY_COVER[cover])
            else:
                if cloud:
                    what = CLOUD_TYPE[cloud]
                elif cover != "OVC":
                    what = _("CLOUDS")
                else:
                    what = ""
                if cover == "VV":
                    text_list.append(_("VERTICAL_VISIBILITY").format(SKY_COVER[cover], what, str(_height)))
                else:
                    text_list.append(_("SKY_COVER").format(SKY_COVER[cover], what, str(_height)))
        if debug: print(sep.join(text_list).replace(';', ':', 1))
        return sep.join(text_list).replace(';', ':', 1)

    def _decodeTempDewPoint(self, d, sep="; "):
        text_list = []
        temp = d['temp']
        dewpt = d['dewpt']
        if temp and temp != "//" and temp != "XX" and temp != "MM":
            temp = temperature(temp)
            text_list.append(_("TEMPERATURE").format(temp.string("C")))
        if dewpt and dewpt != "//" and dewpt != "XX" and dewpt != "MM":
            dewpt = temperature(dewpt)
            text_list.append(_("DEWPOINT").format(dewpt.string("C")))

        if debug: print(sep.join(text_list))
        return sep.join(text_list)

    def _decodePressure(self, d):
        press = d['press']
        if press != '////':
            press = float(press.replace('O', '0'))
            if d['unit']:
                if d['unit'] == 'A' or (d['unit2'] and d['unit2'] == 'INS'):
                    press = pressure(press / 100, 'IN')
                elif d['unit'] == 'SLP':
                    if press < 500:
                        press = press / 10 + 1000
                    else:
                        press = press / 10 + 900
                    press = pressure(press, 'MB')
                elif d['unit'] == 'Q':
                    press = pressure(press, 'HPA')
                else:
                    press = pressure(press, 'MB')
            elif press > 2500:
                press = pressure(press / 100, 'IN')
            else:
                press = pressure(press, 'MB')
            text = _("PRESSURE").format(press)
            if debug: print(text)
        return text

    def _decodeRecent(self, d):
        return _("RECENT") + " " + self._decodePresentWeather(d)

    def _decodeWindShear(self, d):
        text = _("WIND_SHEAR")
        windsahre = "; ".join(d)
        if windsahre == "ALL":
            windsahre = _("ALL_RUNWAY")
        return text + ": " + windsahre

    def _decodeTempExtremum(self, d, sep="; "):
        text_list = []
        for extr, temp, date, hour in d:
            temp = temperature(temp)
            if extr == 'TX':
                text_list.append(_("MAXIMUM_TEMPERATURE_PREDICTED").format(temp.string("C"), date, hour))
            elif extr == 'TN':
                text_list.append(_("MINIMUM_TEMPERATURE_PREDICTED").format(temp.string("C"), date, hour))
        return sep.join(text_list)

    def _decodeRunwayState(self, d, sep="; "):
        text_list = []
        rwy_state = d
        special = rwy_state["special"]
        name = rwy_state["name"]

        if name:
            runway = rwy_state["runway"]
            deposit = rwy_state["deposit"]
            extent = rwy_state["extent"]
            depth = rwy_state["depth"]
            friction = rwy_state["friction"]

            name_n = int(name)

            if runway == "L" or runway == "R" or runway == "C":
                name += " " + RUNWAY[runway]
            elif name == "99" or name == "88":
                name = RUNWAY[name]
            else:
                if name_n < 37: name += " " + RUNWAY["L"]
                if name_n > 49 and name < 87: name += " " + RUNWAY["R"]
            name = _("RUNWAY_STATE_OF") + " " + name
            text_list.append(name)
            if special and special == "CLRD":
                text_list.append(_("CLRD"))
                friction_s = rwy_state["friction_s"]
                if friction_s:
                    if friction_s in FRICTION_TYPE:
                        text_list.append(FRICTION_TYPE[friction_s])
                    else:
                        text_list.append(_("FRICTION_COEFFICIENT").format(int(friction_s) / 100))
            else:
                if deposit:
                    text_list.append(DEPOSIT_TYPE[deposit])
                if extent:
                    text_list.append(EXTENT_TYPE[extent])
                if depth:
                    if depth in DEPTH_TYPE:
                        text_list.append(DEPTH_TYPE[depth])
                    else:
                        text_list.append(_("DEPTH_MM").format(depth))
                if friction:
                    if friction in FRICTION_TYPE:
                        text_list.append(FRICTION_TYPE[friction])
                    else:
                        text_list.append(_("FRICTION_COEFFICIENT").format(int(friction) / 100))
        elif special and special == 'SNOCLO':
            text_list.append(_("SNOCLO"))

        return sep.join(text_list).replace(';', ':', 1)

    def decode(self, d):
        lines = []
        text = ""
        indent = " "
        try:
            for item in d:
                if 'prob' in item:
                    text = self._decodeTypeForecast(item['prob'])
                if 'type' in item:
                    text += self._decodeTypeForecast(item['type'])
                if 'valid' in item:
                    text += indent + self._decodeForecastDateTime(item['valid'])
                if 'wind' in item:
                    lines.append(indent * 2 + self._decodeWind(item['wind']))
                elif not 'min_vis' in item and 'vis' in item:
                    lines.append(indent * 2 + self._decodeVisibility(item['vis']))
                elif 'min_vis' in item:
                    lines.append(
                        indent * 2 + self._decodeVisibility(item['vis']) + self._decodeVisibility(item['min_vis'], 'min'))
                elif 'runway' in item:
                    lines.append(indent * 2 + self._decodeRunwayVisibility(item['runway']))
                elif 'weather' in item:
                    lines.append(indent * 2 + self._decodePresentWeather(item['weather']))
                elif 'sky' in item:
                    lines.append(indent * 2 + self._decodeSkyConditions(item['sky']))
                elif 'tempdewpt' in item:
                    lines.append(indent * 2 + self._decodeTempDewPoint(item['tempdewpt']))
                elif 'press' in item:
                    lines.append(indent * 2 + self._decodePressure(item['press']))
                elif 'windshear' in item:
                    lines.append(indent * 2 + self._decodeWindShear(item['windshear']))
                elif 'temp_extr' in item:
                    lines.append(indent * 2 + self._decodeTempExtremum(item['temp_extr']))
                elif 'recent' in item:
                    lines.append(indent * 2 + self._decodeRecent(item['recent']))
                elif 'runway_state' in item:
                    lines.append(indent * 2 + self._decodeRunwayState(item['runway_state']))
            lines.insert(0, text)
            return "\n".join(lines)
        except Exception as err:
            return DecodeError(" failed while decoding report" + " ".join(err.args) +" ")

    def string(self):
        indent = " "
        d = self.mt
        lines = []
        try:
            if d.type:
                text = self._decodeType()
                if d.station_id:
                    text += self._decodeIndexAirport(d.station_id)
                if d.nil:
                    text += indent + self._decodeNil(d.nil)
                if d.datetime:
                    text += indent + self._decodeDateTime(d.datetime)
                if d.period_taf:
                    text += indent + self._decodeForecastDateTime(d.period_taf)
                lines.append(text)
                if d.wind:
                    lines.append(indent + self._decodeWind(d.wind))
                if not d.min_vis and d.vis:
                    lines.append(indent + self._decodeVisibility(d.vis))
                if d.min_vis:
                    lines.append(indent + self._decodeVisibility(d.vis) + self._decodeVisibility(d.min_vis, 'min'))
                if d.runway:
                    lines.append(indent + self._decodeRunwayVisibility(d.runway))
                if d.weather:
                    lines.append(indent + self._decodePresentWeather(d.weather))
                if d.sky:
                    lines.append(indent + self._decodeSkyConditions(d.sky))
                if d.tempdewpt:
                    lines.append(indent + self._decodeTempDewPoint(d.tempdewpt))
                if d.press:
                    lines.append(indent + self._decodePressure(d.press))
                if d.windshear:
                    lines.append(indent + self._decodeWindShear(d.windshear))
                if d.temp_extr:  # TODO check and change sequence
                    lines.append(indent + self._decodeTempExtremum(d.temp_extr))
                if d.recent:
                    lines.append(indent + self._decodeRecent(d.recent))
                if d.runway_state:
                    lines.append(indent + self._decodeRunwayState(d.runway_state))
                for forecast in d._forecasts_list:
                    lines.append(" " + self.decode(forecast))

            return "\n".join(lines)

        except Exception as err:
            return DecodeError(" failed while decoding report" + " ".join(err.args))

    def report_type(self):
        if self.mt.type == None:
            text = _('UNKNOWN_TYPE')
        elif self.mt.type in REPORT_TYPE:
            text = REPORT_TYPE[self.mt.type]
        else:
            text = self.mt.type + " report"
        if self.mt.mod:
            if self.mt.mod in REPORT_TYPE:
                text += REPORT_TYPE[self.mt.mod]
            else:
                text += self.mt.mod
        if self.datetime:
            text += self.datetime
        if self.forecastperiod:
            text += self.forecastperiod
        return text

    def visibility(self, units=None):
        if self.mt.vis == None:
            return "missing"
        if self.vis_dir:
            text = "%s to %s" % (self.mt.vis.string(units), self.vis_dir.compass())
        else:
            text = self.mt.string(units)
        if self.max_vis:
            if self.max_vis_dir:
                text += "; %s to %s" % (self.max_vis.string(units), self.max_vis_dir.compass())
            else:
                text += "; %s" % self.max_vis.string(units)
        return text

