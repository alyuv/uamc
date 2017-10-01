import re
import datetime

# Exceptions
class ParserError(Exception):
    """Exception raised when an unparseable group is found in body of the report."""
    pass


MISSING_RE = re.compile(r"^[M/]+$")

TYPE_RE = re.compile(r"^(?P<type>METAR|SPECI|TAF)\s+")

MODIFIER_RE = re.compile(r"^(?P<mod>AUTO|FINO|NIL|TEST|CORR?|RTD|COR|CC[A-G])\s+")

STATION_RE = re.compile(r"^(?P<station>[A-Z]{4})\s+")

NIL_RE = re.compile(r"^(?P<nil>NIL)=?\s+")

TIME_RE = re.compile(r"""^(?P<day>\d\d)
                          (?P<hour>\d\d)
                          (?P<min>\d\d)Z?\s+""",
                     re.VERBOSE)

PERIOD_FORECAST_RE = re.compile(r"""^(?P<from_day>\d\d)
                              (?P<from_hour>\d\d)
                              (?P<separate>\/)
                              (?P<till_day>\d\d)
                              (?P<till_hour>\d\d)\s+""",
                                re.VERBOSE)

WIND_RE = re.compile(r"""^(?P<dir>[\dO]{3}|[0O]|///|MMM|VRB)
                          (?P<speed>P?[\dO]{2,3}|[/M]{2,3})
                        (G(?P<gust>P?(\d{1,3}|[/M]{1,3})))?
                          (?P<units>KTS?|LT|K|T|KMH|MPS)?
                      (\s+(?P<varfrom>\d\d\d)V
                          (?P<varto>\d\d\d))?\=?\s+""",
                     re.VERBOSE)

VISIBILITY_RE = re.compile(r"""^(?P<vis>(?P<dist>(M|P)?\d\d\d\d|////)
                                        (?P<dir>[NSEW][EW]?|NDV)?|
                                        (?P<distu>(M|P)?(\d+|\d\d?/\d\d?|\d+\s+\d/\d))
                                        (?P<units>SM|KM|M|U)|
                                        CAVOK )\=?\s+""",
                           re.VERBOSE)

RUNWAY_RE = re.compile(r"""^(RVRNO |
                             R(?P<name>\d\d(RR?|LL?|C)?)/
                              (?P<low>(M|P)?\d\d\d\d)
                            (V(?P<high>(M|P)?\d\d\d\d))?
                              (?P<unit>FT)?[/NDU]*)\=?\s+""",
                       re.VERBOSE)

WEATHER_RE = re.compile(r"""^(?P<int>(-|\+|VC)*)
                             (?P<desc>(MI|PR|BC|DR|BL|SH|TS|FZ)+)?
                             (?P<prec>(DZ|RA|SN|SG|IC|PL|GR|GS|UP|/)*)
                             (?P<obsc>BR|FG|FU|VA|DU|SA|HZ|PY)?
                             (?P<other>PO|SQ|FC|SS|DS|NSW|/+)?
                             (?P<int2>[-+])?\=?\s+""",
                        re.VERBOSE)
SKY_RE = re.compile(r"""^(?P<cover>VV|CLR|SKC|SCK|NSC|NCD|BKN|SCT|FEW|[O0]VC|///)
                        (?P<height>[\dO]{2,4}|///)?
                        (?P<cloud>([A-Z][A-Z]+|///))?\=?\s+""",
                    re.VERBOSE)
PRESS_RE = re.compile(r"""^(?P<unit>A|Q|QNH|SLP)?
                           (?P<press>[\dO]{3,4}|////)
                           (?P<unit2>INS)?\=?\s+""",
                      re.VERBOSE)

TEMP_RE = re.compile(r"""^(?P<temp>(M|-)?\d+|//|XX|MM)/
                          (?P<dewpt>(M|-)?\d+|//|XX|MM)?\=?\s+""",
                     re.VERBOSE)

TEMP_EXTR_RE = re.compile(r"""^(?P<extr>TX|TN)
                               (?P<temp>(M|-)?\d\d|//|XX|MM)/
                               (?P<date>\d\d)
                               (?P<hour>\d\d)Z?\=?\s+""",
                          re.VERBOSE)

RECENT_RE = re.compile(r"""^RE(?P<desc>MI|PR|BC|DR|BL|SH|TS|FZ)?
                              (?P<prec>(DZ|RA|SN|SG|IC|PL|GR|GS|UP)*)?
                              (?P<obsc>BR|FG|FU|VA|DU|SA|HZ|PY)?
                              (?P<other>PO|SQ|FC|SS|DS)?\=?\s+""",
                       re.VERBOSE)

WINDSHEAR_RE = re.compile(r"^(WS\s+)?(ALL\s+RWY|RWY(?P<name>\d\d(R?|L?|C)?))\=?\s+")

COLOR_RE = re.compile(r"""^(BLACK)?(BLU|GRN|WHT|RED)\+?
                        (/?(BLACK)?(BLU|GRN|WHT|RED)\+?)*\s*""",
                      re.VERBOSE)

RUNWAYSTATE_RE_1 = re.compile(r"""((?P<name>\d\d) | R(?P<namenew>\d\d)(RR?|LL?|C)?/?)
                                ((?P<special> SNOCLO|CLRD(\d\d|//)) |
                                 (?P<deposit>(\d|/))
                                 (?P<extent>(\d|/))
                                 (?P<depth>(\d\d|//))
                                 (?P<friction>(\d\d|//)))\s+""",
                              re.VERBOSE)

RUNWAYSTATE_RE = re.compile(r"""R?(?P<name>\d?\d?)(?P<runway>(L|R|C)?)(?P<separate>\/?)
                                  ((?P<special>SNOCLO|CLRD)(?P<friction_s>(\d\d|//)?)|
                                  (?P<deposit>(\d|/))
                                  (?P<extent>(\d|/))
                                  (?P<depth>(\d\d|//))
                                  (?P<friction>(\d\d|//)))\=?\s+""",
                            re.VERBOSE)

FORECAST_RE = re.compile(r"^((?P<prob>PROB30|PROB40)\s+)?(?P<type>TEMPO|BECMG|FCST|NOSIG)\=?\s+")

FORECAST_VALID_RE = re.compile(r"""^(?P<from_day>\d\d)
                              (?P<from_hour>\d\d)
                              (?P<separate>\/)
                              (?P<till_day>\d\d)
                              (?P<till_hour>\d\d)\s+""",
                               re.VERBOSE)

TRENDTIME_RE = re.compile(r"(?P<when>(FM|TL|AT))(?P<hour>\d\d)(?P<min>\d\d)\s+")

REMARK_RE = re.compile(r"^(RMKS?|NOSPECI|NOSIG)\=?\s+")

AUTO_RE = re.compile(r"^AO(?P<type>\d)\s+")

SEALVL_PRESS_RE = re.compile(r"^SLP(?P<press>\d\d\d)\s+")

PEAK_WIND_RE = re.compile(r"""^P[A-Z]\s+WND\s+
                               (?P<dir>\d\d\d)
                               (?P<speed>P?\d\d\d?)/
                               (?P<hour>\d\d)?
                               (?P<min>\d\d)\s+""",
                          re.VERBOSE)

WIND_SHIFT_RE = re.compile(r"""^WSHFT\s+
                                (?P<hour>\d\d)?
                                (?P<min>\d\d)
                                (\s+(?P<front>FROPA))?\s+""",
                           re.VERBOSE)

PRECIP_1HR_RE = re.compile(r"^P(?P<precip>\d\d\d\d)\s+")

PRECIP_24HR_RE = re.compile(r"""^(?P<type>6|7)
                                 (?P<precip>\d\d\d\d)\s+""",
                            re.VERBOSE)

PRESS_3HR_RE = re.compile(r"""^5(?P<tend>[0-8])
                                (?P<press>\d\d\d)\s+""",
                          re.VERBOSE)

TEMP_1HR_RE = re.compile(r"""^T(?P<tsign>0|1)
                               (?P<temp>\d\d\d)
                               ((?P<dsign>0|1)
                               (?P<dewpt>\d\d\d))?\s+""",
                         re.VERBOSE)

TEMP_6HR_RE = re.compile(r"""^(?P<type>1|2)
                              (?P<sign>0|1)
                              (?P<temp>\d\d\d)\s+""",
                         re.VERBOSE)

TEMP_24HR_RE = re.compile(r"""^4(?P<smaxt>0|1)
                                (?P<maxt>\d\d\d)
                                (?P<smint>0|1)
                                (?P<mint>\d\d\d)\s+""",
                          re.VERBOSE)

UNPARSED_RE = re.compile(r"(?P<group>\S+)\s+")

LIGHTNING_RE = re.compile(r"""^((?P<freq>OCNL|FRQ|CONS)\s+)?
                             LTG(?P<type>(IC|CC|CG|CA)*)
                                ( \s+(?P<loc>( OHD | VC | DSNT\s+ | \s+AND\s+ |
                                 [NSEW][EW]? (-[NSEW][EW]?)* )+) )?\s+""",
                          re.VERBOSE)

TS_LOC_RE = re.compile(r"""TS(\s+(?P<loc>( OHD | VC | DSNT\s+ | \s+AND\s+ |
                                           [NSEW][EW]? (-[NSEW][EW]?)* )+))?
                                          ( \s+MOV\s+(?P<dir>[NSEW][EW]?) )?\s+""",
                       re.VERBOSE)


def _report_match(handler, match):
    if match:
        print(handler.__name__, " matched -> '" + match + "'")
    else:
        print(handler.__name__, " didn't match...")

def _unparsedGroup(self, d):
    self._unparsed_groups.append(d['group'])

debug = False


class MetarTaf(object):

    def __init__(self, metartafcode, month=None, year=None, utcdelta=None):
        self.code = metartafcode
        self.type = None
        self.mod = None
        self.station_id = None
        self.nil = None
        self.time = None
        self.datetime = {}
        self.period_taf = {}
        self.cycle = None
        self.wind_dir = None
        self.wind_speed = None
        self.wind_gust = None
        self.wind_dir_from = None
        self.wind_dir_to = None
        self.wind = {}
        self.vis = {}
        self.min_vis = {}

        self.vis_dir = None
        self.vis_max = None
        self.vis_dir_max = None
        self.vis_units = None

        self.temp = None
        self.temp_extr = []
        self.dewpt = None
        self.tempdewpt = {}
        self.press = None
        self.runway = []
        self.weather = []
        self.recent = []
        self.sky = []  #
        self.windshear = []
        self.wind_speed_peak = None
        self.wind_dir_peak = None
        self.peak_wind_time = None
        self.wind_shift_time = None
        self.runway_state = {}

        self.max_temp_6hr = None
        self.min_temp_6hr = None
        self.max_temp_24hr = None
        self.min_temp_24hr = None

        self.press_sea_level = None
        self.precip_1hr = None
        self.precip_3hr = None
        self.precip_6hr = None
        self.precip_24hr = None

        self.temp1hr = {}
        self.temp6hr = {}
        self.temp24hr = {}
        self.press3hr = {}
        self.peak_wind = {}
        self.wind_shift = {}
        self.lightning = {}
        self.tsl_loc = {}
        self.auto_remark = {}

        self._forecast = False
        self._forecast_type = ''
        self._unparsed_forecasts = []
        self._forecast_groups = []
        self._forecasts_list = []

        self._forecasts_groups = []

        self._trend = False
        self._trend_groups = []

        self._remarks = []

        self._unparsed_groups = []
        self._unparsed_remarks = []

        self._now = datetime.datetime.utcnow()
        if utcdelta:
            self._utcdelta = utcdelta
        else:
            self._utcdelta = datetime.datetime.now() - self._now

        self._month = month
        self._year = year

        code = self.code + " "
        try:
            ngroup = len(MetarTaf.handlers)
            igroup = 0
            ifailed = -1
            while igroup < ngroup and code:
                pattern, handler, repeatable = MetarTaf.handlers[igroup]
                if debug: print(handler.__name__, ":", code)
                m = pattern.match(code)
                while m:
                    ifailed = -1
                    if debug: _report_match(handler, m.group())
                    handler(self, m.groupdict())
                    code = code[m.end():]
                    # if forecast
                    if self._forecast:
                        code = self._do_forecast_handlers(code)
                        self._forecast = False
                    if not repeatable: break
                    if debug: print(handler.__name__, ":", code)
                    m = pattern.match(code)
                if not m and ifailed < 0:
                    ifailed = igroup
                igroup += 1
                if igroup == ngroup and not m:
                    if debug: print("** it's not a main-body group **")
                    pattern, handler = (UNPARSED_RE, _unparsedGroup)
                    if debug: print(handler.__name__, ":", code)
                    m = pattern.match(code)
                    if m:
                        if debug: _report_match(handler, m.group())
                        handler(self, m.groupdict())
                        code = code[m.end():]
                    igroup = ifailed
                    ifailed = -2

        except Exception as err:
            raise ParserError(handler.__name__ + " failed while processing '" + code + "'\n" + " ".join(err.args))
            raise err
        if self._unparsed_groups:
            code = ' '.join(self._unparsed_groups)

    def _do_forecast_handlers(self, code):
        for pattern, handler, repeatable in MetarTaf.forecast_handlers:
            if debug: print(handler.__name__, ":", code)
            m = pattern.match(code)
            while m:
                if debug: _report_match(handler, m.group())
                handler(self, m.groupdict())
                code = code[m.end():]
                if not repeatable: break
                m = pattern.match(code)
        if self._forecast_groups:
            self._forecasts_list.append(self._forecast_groups)
            self._forecast_groups = []
        return code

    def _do_trend_handlers(self, code):
        for pattern, handler, repeatable in MetarTaf.trend_handlers:
            if debug: print(handler.__name__, ":", code)
            m = pattern.match(code)
            while m:
                if debug: _report_match(handler, m.group())
                self._trend_groups.append(m.group().strip())
                handler(self, m.groupdict())
                code = code[m.end():]
                if not repeatable: break
                m = pattern.match(code)
        return code

    def _handleType(self, d):
        self.type = d['type']

    def _handleStation(self, d):
        self.station_id = d['station']

    def _handleModifier(self, d):
        self.mod = d['mod']

    def _handleNil(self, d):
        self.nil = d

    def _handleTime(self, d):
        self.datetime = d

    def _handlePeriodForecast(self, d):
        self.period_taf = d
        return d

    def _handleWind(self, d):
        self.wind = d
        return d

    def _handleVisibility(self, d):
        if self.vis:
            self.min_vis = d
        else:
            self.vis = d

    def _handleRunway(self, d):
        if d['name']:
            name = d['name']
            low = d['low']
            if d['high']:
                high = d['high']
            else:
                high = low
            self.runway.append((name, low, high))

    def _handleWeather(self, d):
        inteni = d['int']
        if not inteni and d['int2']:
            inteni = d['int2']
        desci = d['desc']
        preci = d['prec']
        obsci = d['obsc']
        otheri = d['other']
        self.weather.append((inteni, desci, preci, obsci, otheri))

    def _handleSky(self, d):
        height = d['height']
        if not height or height == "///":
            height = None
        else:
            height = height.replace('O', '0')
            height = height
        cover = d['cover']
        if cover == 'SCK' or cover == 'SKC' or cover == 'CL': cover = 'CLR'
        if cover == '0VC': cover = 'OVC'
        cloud = d['cloud']
        if cloud == '///': cloud = ""
        self.sky.append((cover, height, cloud))

    def _handleTemp(self, d):
        self.tempdewpt = d

    def _handleTempExtr(self, d):
        extr = d['extr']
        temp = d['temp']
        date = d['date']
        hour = d['hour']
        self.temp_extr.append((extr, temp, date, hour))

    def _handlePressure(self, d):
        self.press = d

    def _handleRecent(self, d):
        desci = d['desc']
        preci = d['prec']
        obsci = d['obsc']
        otheri = d['other']
        self.recent.append(("", desci, preci, obsci, otheri))

    def _handleWindShear(self, d):
        if d['name']:
            self.windshear.append(d['name'])
        else:
            self.windshear.append("ALL")

    def _handleColor(self, d):
        pass

    def _handleRunwayState(self, d):
        self.runway_state = d

    def _handleTrend(self, d):
        if 'trend' in d:
            self._trend_groups.append(d['trend'])
        self._trend = True

    # forecasts
    def _handleForecast(self, d):
        if 'type' in d:
            self._forecast_type = d['type']
        self._forecast = True

    def _startForecasts(self, d):
        if 'type' in d:
            self._forecast_groups.append(d)
            self._forecast = True

    def _handleValidForecast(self, d):
        self._forecast_groups.append({'valid': d})

    def _handleWindForecast(self, d):
        self._forecast_groups.append({'wind': d})

    def _handleVisibilityForecast(self, d):
        self._forecast_groups.append({'vis': d})

    def _handleRunwayForecast(self, d):
        self._forecast_groups.append({'runway': d})

    def _handleWeatherForecast(self, d):
        inteni = d['int']
        if not inteni and d['int2']:
            inteni = d['int2']
        desci = d['desc']
        preci = d['prec']
        obsci = d['obsc']
        otheri = d['other']
        weather = (inteni, desci, preci, obsci, otheri)

        is_weather = False
        for item in self._forecast_groups:
            if 'weather' in item:
                item['weather'].append(weather)
                is_weather = True
        if not is_weather:
            self._forecast_groups.append({'weather': [weather]})

    def _handleSkyForecast(self, d):
        height = d['height']
        if not height or height == "///":
            height = None
        else:
            height = height.replace('O', '0')
            height = height
        cover = d['cover']
        if cover == 'SCK' or cover == 'SKC' or cover == 'CL': cover = 'CLR'
        if cover == '0VC': cover = 'OVC'
        cloud = d['cloud']
        if cloud == '///': cloud = ""
        sky = (cover, height, cloud)

        is_sky = False
        for item in self._forecast_groups:
            if 'sky' in item:
                item['sky'].append(sky)
                is_sky = True
        if not is_sky:
            self._forecast_groups.append({'sky': [sky]})

    def _handleTempForecast(self, d):
        self._forecast_groups.append({'tempdewt':d})

    def _handlePressureForecast(self, d):
        self._forecast_groups.append({'press':d})

    def _handleWindShearForecast(self, d):
        windshear = []
        if d['name']:
            windshear.append(d['name'])
        else:
            windshear.append("ALL")

        is_windshear = False
        for item in self._forecast_groups:
            if 'windshear' in item:
                item['windshear'].append(d)
                is_windshear = True
        if not is_windshear:
            self._forecast_groups.append({'windshear': d})

    def _handleRunwayStateForecast(self, d):
        self._forecast_groups.append({'runway_state':d})

    def _handleTempExtrForecast(self, d):
        extr = d['extr']
        temp = d['temp']
        date = d['date']
        hour = d['hour']
        temp_extr= (extr, temp, date, hour)

        is_temp_extr = False
        for item in self._forecast_groups:
            if 'temp_extr' in item:
                item['temp_extr'].append(temp_extr)
                is_temp_extr = True
        if not is_temp_extr:
            self._forecast_groups.append({'temp_extr':[temp_extr]})

    def _startRemarks(self, d):
        self._remarks = []

    def _handleSealvlPressRemark(self, d):
        self.press_sea_level = d

    def _handlePrecip24hrRemark(self, d):
        self.precip_24hr = d

    def _handlePrecip1hrRemark(self, d):
        self.precip_1hr = d

    def _handleTemp1hrRemark(self, d):
        self.temp1hr = d

    def _handleTemp6hrRemark(self, d):
        self.temp6hr = d

    def _handleTemp24hrRemark(self, d):
        self.temp24hr = d

    def _handlePress3hrRemark(self, d):
        self.press3hr = d

    def _handlePeakWindRemark(self, d):
        self.peak_wind = d

    def _handleWindShiftRemark(self, d):
        self.wind_shift = d

    def _handleLightningRemark(self, d):
        self.lightning = d

    def _handleTSLocRemark(self, d):
        self.tsl_loc = d

    def _handleAutoRemark(self, d):
        self.auto_remark = d

    def _unparsedGroup(self, d):
        pass

    def _unparsedRemark(self, d):
        pass

    def _unparsedForecast(self, d):
        pass

    handlers = [(TYPE_RE, _handleType, False),
                (MODIFIER_RE, _handleModifier, False),
                (STATION_RE, _handleStation, False),
                (NIL_RE, _handleNil, False),
                (TIME_RE, _handleTime, False),
                (PERIOD_FORECAST_RE, _handlePeriodForecast, False),
                (WIND_RE, _handleWind, False),
                (VISIBILITY_RE, _handleVisibility, True),
                (RUNWAY_RE, _handleRunway, True),
                (WEATHER_RE, _handleWeather, True),
                (SKY_RE, _handleSky, True),
                (TEMP_RE, _handleTemp, False),
                (PRESS_RE, _handlePressure, True),
                (RECENT_RE, _handleRecent, True),
                (WINDSHEAR_RE, _handleWindShear, True),
                (COLOR_RE, _handleColor, True),
                (RUNWAYSTATE_RE, _handleRunwayState, True),
                (FORECAST_RE, _startForecasts, True)]

    trend_handlers = [(TRENDTIME_RE, _handleTrend, True),
                      (WIND_RE, _handleTrend, True),
                      (VISIBILITY_RE, _handleTrend, True),
                      (WEATHER_RE, _handleTrend, True),
                      (SKY_RE, _handleTrend, True),
                      (COLOR_RE, _handleTrend, True)]

    forecast_handlers = [(FORECAST_VALID_RE, _handleValidForecast, True),
                         (WIND_RE, _handleWindForecast, True),
                         (VISIBILITY_RE, _handleVisibilityForecast, True),
                         (RUNWAY_RE, _handleRunwayForecast, True),
                         (WEATHER_RE, _handleWeatherForecast, True),
                         (SKY_RE, _handleSkyForecast, True),
                         (TEMP_RE, _handleTempForecast, True),
                         (TEMP_EXTR_RE, _handleTempExtrForecast, True),
                         (PRESS_RE, _handlePressureForecast, True),
                         (WINDSHEAR_RE, _handleWindShearForecast, True),
                         (RUNWAYSTATE_RE, _handleRunwayStateForecast, True)
                         ]

    remark_handlers = [(AUTO_RE, _handleAutoRemark),
                       (SEALVL_PRESS_RE, _handleSealvlPressRemark),
                       (PEAK_WIND_RE, _handlePeakWindRemark),
                       (WIND_SHIFT_RE, _handleWindShiftRemark),
                       (LIGHTNING_RE, _handleLightningRemark),
                       (TS_LOC_RE, _handleTSLocRemark),
                       (TEMP_1HR_RE, _handleTemp1hrRemark),
                       (PRECIP_1HR_RE, _handlePrecip1hrRemark),
                       (PRECIP_24HR_RE, _handlePrecip24hrRemark),
                       (PRESS_3HR_RE, _handlePress3hrRemark),
                       (TEMP_6HR_RE, _handleTemp6hrRemark),
                       (TEMP_24HR_RE, _handleTemp24hrRemark),
                       (UNPARSED_RE, _unparsedRemark)]
