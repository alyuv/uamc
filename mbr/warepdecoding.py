import re
from django.utils.translation import gettext as _


class WarepMessage:
    def __init__(self, message, station, valid_begin):
        # message.replace('=','')
        self.message = " ".join(message.split()).replace('=','')  # delete all whitespaces
        self.items =list()
        self.elements = list()
        self.valid_begin = valid_begin
        self.type = ''
        self.error =''
        self.storm = 0  # False ?
        self.title = ''
        self.index = ''
        self.station = station
        self.datetime = ''
        self.datetime_decode = ''
        self.repitition = False
        self.phenomena =''
        self.wind = ''
        self.wind_status = 0
        self.wind_decoded = ''
        self.cloud = ''
        self.cloud_decoded = ''
        self.weather = ''
        self.weather_decoded = ''
        self.weather_status = ''
        self.cloud_status = 0
        self.precipitation = ''
        self.precipitation_decoded = ''
        self.precipitation_status = ''
        self.visibility = ''
        self.visibility_decoded =''
        self.visibility_status = 0
        self.deposits = ''
        self.deposits_decoded = ''
        self.deposits_status = 0
        self.icerain = ''
        self.icerain_decoded = ''
        self.hail = ''
        self.hail_decoded = ''
        self.mounts = ''
        self.mounts_decoded = ''

    def decode(self):
        items = self.message.split(' ')
        self.items = list(items)
        self.elements = list(items)
        self.decodeType(items[0])
        self.decodeTitle(items[1])
        self.decodeIndex(items[2])
        self.decodeDataTime(items[3])
        for i in range(4, len(items)-1):
            if i < (len(items)-2):
                self.decodeSection(items[i], items[i + 1], items[i + 2])
            else:
                self.decodeSection(items[i], items[i + 1])

        return True

    def decodeType(self, item):
        if item == 'STORM':
            self.type = item
            self.storm = 1
        elif item == 'AVIA':
            self.type = item
            self.storm = 0
        else:
            self.type = _('W_UNKNOWNG_TYPE_MESSGE').format(item)

    def decodeTitle(self, item):
        if item == 'WAREP':
            self.title = item
        else:
            self.title = _('W_UNKNOWNG_TITLE_MESSAGE').format(item)

    def decodeIndex(self, item):
        result = re.findall(r'(^3\d{4}\b)', item, re.VERBOSE)
        if result:
            result = result[0]
            self.index = item
        else:
            self.index = _('W_UNKNOWNG_INDEX_STATION').format(item)

    def decodeDataTime(self, item):
        # 0612001
        result = re.findall(r'(\d{2})(\d{2})(\d{2})(\d{1})', item, re.VERBOSE)
        if result:
            result = result[0]
            self.datetime = item
            self.datetime_decode = result[0]+'th on time ' + result[1] +':'+ result[2]
            if result[3] == '0':
                self.repitition = True
        else:
            self.datetime = _('W_DATETIME_SECTION_ERROR').format(item)

    def decodeSection(self, phenomena, section, sectionnext=None):
        self.phenomena += ' ' + phenomena
        self.wind = section
        if phenomena == '11': self.wind_decoded = _('W_WIND'); self.decodeWind(section)
        elif phenomena == '12': self.wind_decoded = _('W_WIND'); self.decodeWind(section)
        elif phenomena == '17': self.wind_decoded = _('W_SQUALL'); self.decodeWind(section)
        elif phenomena == '18': self.wind_decoded = _('W_HEAVY_SQUALL'); self.decodeWind(section)

        elif phenomena == '19': self.wind_decoded = _('W_TORNADO'); self.decodeWind(section); self.decodeTornado(section)

        elif phenomena == '30': self.decodeCloud(section)

        elif phenomena == '36':
            self.decodeWind(section)
            self.decodeVisibility(sectionnext)

        elif phenomena == '40':
            self.decodeVisibility(section)
            if sectionnext:
                self.decodeWind(sectionnext)

        elif phenomena == '41': self.decodeVisibility(section)

        elif phenomena == '50': self.deposits_decoded = _('W_GLAZE'); self.decodeDeposits(section)
        elif phenomena == '51': self.deposits_decoded = _('W_COMPLEX_DEPOSITION'); self.decodeDeposits(section)
        elif phenomena == '52': self.deposits_decoded = _('W_COMPLEX_DEPOSITION'); self.decodeDeposits(section)
        elif phenomena == '53': self.deposits_decoded = _('W_STRONG_GLAZE'); self.decodeDeposits(section)
        elif phenomena == '54': self.deposits_decoded = _('W_HOARFROST'); self.decodeDeposits(section)
        elif phenomena == '55': self.deposits_decoded = _('W_STRONG_COMPLEX_DEPOSITION'); self.decodeDeposits(section)
        elif phenomena == '56': self.deposits_decoded = _('W_COMPLEX_DEPOSITION'); self.decodeDeposits(section)
        elif phenomena == '57': self.deposits_decoded = _('W_SLEET_ON_ROADS'); self.decodeDeposits(section)

        elif phenomena == '61':
            self.precipitation_decoded = _('W_RAIN');
            self.decodePrecipitation(section)
        elif phenomena == '62': self.precipitation_decoded = _('W_INTENSE_RAIN'); self.decodePrecipitation(section)
        elif phenomena == '64': self.precipitation_decoded = _('W_INTENSE_RAIN'); self.decodePrecipitation(section)
        elif phenomena == '65': self.precipitation_decoded = _('W_INTENSE_RAIN'); self.decodePrecipitation(section)
        elif phenomena == '66': self.precipitation_decoded = _('W_INTENSE_RAIN'); self.decodePrecipitation(section)
        elif phenomena == '71': self.precipitation_decoded = _('W_HEAVY_SNOW'); self.decodePrecipitation(section)
        elif phenomena == '75': self.precipitation_decoded = _('W_HEAVY_SNOW'); self.decodePrecipitation(section)

        elif phenomena == '68': self.weather_decoded = _('W_ICE_RAIN'); self.decodeTemperature(section)

        elif phenomena == '91': self.weather_decoded = _('W_THUNDERSTORM'); self.decodeThunderstorm(section)

        elif phenomena == '78': self.wind_decoded = _('W_SNOWSTORM'); self.decodeWind(section)

        elif phenomena == '90': self.decodeHail(section)
        elif phenomena == '92': self.decodeHail(section)
        elif phenomena == '95': self.decodeMounts(section)
        else:
            pass

    def decodeWind(self, item):
        result = re.findall(r'^1([0-9]{2})(\S\S)([0-9]{2})', item, re.VERBOSE)
        if result:
            self.wind = item
            result = list(result[0])
            self.wind_decoded += _('W_WIND_DIRECT_SPEED_GUST').format(int(result[0]) * 10, result[1], result[2])
            self.wind_status = self.storm
        elif item !='':
            self.decodeCloud(item)
        else:
            self.wind_decoded += _('W_WIND_SECTION_ERROR').format(item)

    def decodeTornado(self,item):
        result = re.findall(r'^2([0-9]{2})([0-9]{2}$)', item, re.VERBOSE)
        if result:
            self.wind = item
            result = list(result[0])
            self.decodeWeather(result[1])
            self.weather_decoded += _('W_WIND_TORNADO_DIRECTION').format(result[2])
        else:
            self.weather_decoded += _('W_FINISH')

    def decodePrecipitation(self, item):
        result = re.findall(r'^3([0-9]{3})([0-9]{2})', item, re.VERBOSE)
        if result:
            self.precipitation = item
            result = list(result[0])
            if result[0] == '000': result[0] = 'Not used'
            elif result[0] == '988': result[0] = '988'
            elif result[0] == '989': result[0] = '989'
            elif result[0] == '990': result[0] = 'Trace' #TODO translate
            elif result[0] == '991': result[0] = '0.1'
            elif result[0] == '991': result[0] = '0.1'
            elif result[0] == '992': result[0] = '0.2'
            elif result[0] == '993': result[0] = '0.3'
            elif result[0] == '994': result[0] = '0.4'
            elif result[0] == '995': result[0] = '0.5'
            elif result[0] == '996': result[0] = '0.6'
            elif result[0] == '997': result[0] = '0.7'
            elif result[0] == '998': result[0] = '0.8'
            elif result[0] == '999': result[0] = '0.9'
            elif result[0] == '///': result[0] = _('W_NOT_MESSURED')
            else: result[0] = '{0:.1f}'.format(int(result[0])*0.1)
            self.precipitation_decoded += _('W_PRECIPITATION_AMOUNT').format(result[0],result[1])
            self.precipitation_status = self.storm
        else: #TODO:check
            self.precipitation_decoded = _('W_PRECIPITATION_SECTION_ERROR').format(item)

    def decodeVisibility(self, item):
        result = re.findall(r'^7([0-9]{2})([0-9]{2})(\S\S)', item, re.VERBOSE)
        if result:
            self.visibility = item
            result = list(result[0])
            if result[0] == '00': vis = '<100' +_('W_METERS')
            elif (int(result[0]) <= 50): vis = str(int(result[0]) * 100) + _('W_METERS')  # W_METERS;
            elif (int(result[0]) >= 56 and int(result[1]) <= 80): vis = str(int(result[0]) - 50) + ('W_KM') # '{0:.1f}'.format(int(block[0])*0.1)
            elif result[0] == '91': vis = ' 50' + _('W_METERS')
            elif result[0] == '92': vis = '200' + _('W_METERS')
            elif result[0] == '93': vis = '500' + _('W_METERS')
            elif result[0] == '94': vis = '1 km' + _('W_KM')
            elif result[0] == '95': vis = '2 km' + _('W_KM')
            elif result[0] == '96': vis = '4 km' + _('W_KM')
            elif result[0] == '97': vis = '10 km' + _('W_KM')
            elif result[0] == '98': vis = '20 km' + _('W_KM')
            elif result[0] == '99': vis = '50 km' + _('W_KM')
            self.visibility_decoded = _('W_VISIBILITY') + vis
            self.decodeWeather(result[1])
            if result[2] != '//': self.weather += _('W_TIME').format(result[2])
            self.visibility_status = self.storm
        else:
            self.visibility_decoded = _('W_VISIBILITY_SECTION_ERROR').format(item)

    def decodeDeposits(self, item):
        result = re.findall(r'^([0-9\/]{2})([0-9]{1})([0-9]{2})([0-9]{1})', item, re.VERBOSE)
        if result:
            self.deposits = item
            result = list(result[0])
            if result[0]  == '//': result[0] = _('W_BEGINNING')
            result[1] = '-' if result[1] == '0' else '+'
            result[3] = _('W_INCREASE') if result[3] == '1' else _('W_SAVING')
            if result[0] != _('W_BEGINNING'):
                if int(result[0]) >= 55:
                    self.deposits_decoded += _('W_DEP_MORE').format(result[1], result[2], result[3])
                else:
                    self.deposits_decoded += _('W_DEP').format(result[0], result[1], result[2], result[3])
            self.deposits_status = self.storm
        else:
            self.deposits_decoded += _('W_FINISH')
            self.deposits_status = self.storm

    def decodeCloud(self, item):
        result = re.findall(r'^8(\d)(\d)([0-9]{2})', item, re.VERBOSE)
        if result:
            self.cloud = item
            result = list(result[0])
            if result[0] == '0': self.cloud_decoded = _('W_NO_CLOUDS 0')
            elif result[0] == '1': self.cloud_decoded = _('W_CLOUDS').format('1')
            elif result[0] == '2': self.cloud_decoded = _('W_CLOUDS').format('2-3')
            elif result[0] == '3': self.cloud_decoded = _('W_CLOUDS').format('4')
            elif result[0] == '4': self.cloud_decoded = _('W_CLOUDS').format('5')
            elif result[0] == '5': self.cloud_decoded = _('W_CLOUDS').format('6')
            elif result[0] == '6': self.cloud_decoded = _('W_CLOUDS').format('7-8')
            elif result[0] == '7': self.cloud_decoded = _('W_CLOUDS').format('9')
            elif result[0] == '8': self.cloud_decoded = _('W_CLOUDS').format('10')
            elif result[0] == '9': self.cloud_decoded = _('W_LOW_VISIBILITY')
            elif result[0] == '\/': self.cloud_decoded = _('W_CLOUD_COVER')
            if result[1] == '0': self.cloud_decoded += _('W_CIRRUS')
            elif result[1] == '1': self.cloud_decoded += _('W_CIRROCUMULUS')
            elif result[1] == '2': self.cloud_decoded += _('W_CIRROSTRATUS')
            elif result[1] == '3': self.cloud_decoded += _('W_ALTOCUMULUS')
            elif result[1] == '4': self.cloud_decoded += _('W_ALTOSTRATUS')
            elif result[1] == '5': self.cloud_decoded += _('W_NIMBOSTRATUS')
            elif result[1] == '6': self.cloud_decoded += _('W_STRATOCUMULUS')
            elif result[1] == '7': self.cloud_decoded += _('W_STRATUS')
            elif result[1] == '8': self.cloud_decoded += _('W_CUMULUS')
            elif result[1] == '9': self.cloud_decoded += _('W_CUMULONIMBUS')
            elif result[1] == '\/': self.cloud_decoded += _('W_CLOUD_NOT')
            self.cloud_decoded += _('W_CLOUD_HEIGHT').format(int(result[2]) * 10)
            self.cloud_status = self.storm
        else:
            self.cloud_decoded = _('W_CLOUD_SECTION_ERROR').format(item)

    def decodeTemperature(self, item):
        result = re.findall(r'^(\d)(\d\d)', item, re.VERBOSE)
        if result:
            self.icerain = item
            result = list(result[0])
            result[0] = '-' if result[0] == '0' else '+'
            self.weather_decoded += _('W_TEMPERATURE').format(result[0], result[1])
        else:
            self.weather_decoded = _('INCORECT_TEMPERATURE_SECTION').format(item)

    def decodeThunderstorm(self,item):
        result = re.findall(r'^(\d)(\d\d)$', item, re.VERBOSE)
        if result:
            self.temp = item
            result = list(result[0])
            result[2] = '-'+result[2] if result[1] == '0' else '+' + result[2]
            self.weather_decoded += _('W_TEMP').format(result[2])
            self.weather_status += _('W_FINISH')
        else:
            self.weather_status = self.storm

    def decodeHail(self, item):
        result = re.findall(r'^(932)([0-9]{2})', item, re.VERBOSE)
        if result:
            self.hail = item
            result = list(result[0])
            hail = int(result[1])
            self.hail_decoded = _('W_HAIL').format(result[1]) if hail < 55 else _('W_HAIL_MORE') # Hail more than 50mm.
        else:
            self.hail_decoded = _('W_INCORECT_HAIL_BLOCK').format(item)

    def decodeMounts(self, item):

        result = re.findall(r'(^950)(\d)(\d)', item, re.VERBOSE)
        if result:
            self.mounts = item
            result = list(result[0])
            if result[1] == '0': mounts = _('W_ALL_MOUNTAINS_OPEN')
            elif result[1] == '1': mounts = _('W_MOUNTAINS_PARTLY')
            elif result[1] == '2': mounts = _('W_ALL_MOUNTAIN_SLOPES')
            elif result[1] == '3': mounts = _('W_MOUNTAINS_OPEN')
            elif result[1] == '4': mounts = _('W_CLOUDS_LOW_OPEN')
            elif result[1] == '5': mounts = _('W_CLOUDS_LOW')
            elif result[1] == '6': mounts = _('W_ALL_PEAKS_COVERED')
            elif result[1] == '7': mounts = _('W_MOUNTAINS_GENERALLYLY')
            elif result[1] == '8': mounts = _('W_ALL_PEAKS_PASSES')
            elif result[1] == '9': mounts = _('W_MOUNTAINS_CANNOT_BE_SEEN')
            if result[2] == '0': mounts += _(' W_NO_CHANGE')
            elif result[2] == '1': mounts += _(' W_CUMULIFICATION')
            elif result[2] == '2': mounts += _(' W_SLOW_ELEVATION')
            elif result[2] == '3': mounts += _(' W_RAPID_ELEVATION')
            elif result[2] == '4': mounts += _(' W_ELEVATION')
            elif result[2] == '5': mounts += _(' W_SLOW_LOWERING')
            elif result[2] == '6': mounts += _(' W_RAPID_LOWERING')
            elif result[2] == '7': mounts += _(' W_STRATIFICATION')
            elif result[2] == '8': mounts += _(' W_STRATIFICATION_LOWERING')
            elif result[2] == '9': mounts += _(' W_RAPID_CHANGE')
            self.mounts_decoded = mounts
        else:
            self.mounts_decoded = _('W_INCORRECT_MOUNTS_SECTION').format(item)

    def decodeWeather(self,item):
        if item == '00': self.weather = 'Cloud development not observed or not observable'
        elif item == '01': self.weather = 'Clouds generally dissolving or becoming less developed'
        elif item == '02': self.weather_decoded = 'State of sky on the whole unchanged'
        elif item == '03': self.weather_decoded = 'Clouds generally forming or developing'
        elif item == '04': self.weather_decoded = 'Visibility reduced by smoke,e.g. veldt or forest fires, industrial smoke or volcanic ashes'
        elif item == '05': self.weather_decoded = 'Haze'
        elif item == '06': self.weather_decoded = 'Widespread dust in suspension in the air, not raised by wind at or near the station at the time of observation'
        elif item == '07': self.weather_decoded = 'Dust or sand raised by wind at or near the station at the time of observation, but no well-developed dust whirl(s) or sand whirl(s), and no duststorm, or sandstorm seen; or, in the case of ships, blowing spray at the station'
        elif item == '08': self.weather_decoded = 'Well-developed dust whirl(s) or sand whirl(s) seen at or near the station during the preceding hour or at the time of observation, but no duststorm or sandstorm'
        elif item == '09': self.weather_decoded = 'Duststorm or sandstorm within sight at the time of observation, or at the station during the preceding hour'
        elif item == '10': self.weather_decoded = 'Mist'
        elif item == '11': self.weather_decoded = 'Patches'
        elif item == '12': self.weather_decoded = 'More or less continuous'
        elif item == '13': self.weather_decoded = 'Lightning visible, no thunder heard'
        elif item == '14': self.weather_decoded = 'Precipitation within sight, not reaching the ground or the surface of the sea'
        elif item == '15': self.weather_decoded = 'Precipitation within sight, reaching the ground or the surface of the sea, but distant, i.e. estimated to be more than 5 km from the station'
        elif item == '16': self.weather_decoded = 'Precipitation within sight, reaching the ground or the surface of the sea, near to, but not at the station'
        elif item == '17': self.weather_decoded = 'Thunderstorm, but no precipitation at the time of observation'
        elif item == '18': self.weather_decoded = 'Squalls'
        elif item == '19': self.weather_decoded = 'Funnel cloud(s)'
        elif item == '20': self.weather_decoded = 'Drizzle (not freezing) or snow grains'
        elif item == '21': self.weather_decoded = 'Rain (not freezing'
        elif item == '22': self.weather_decoded = 'Snow'
        elif item == '23': self.weather_decoded = 'Rain and snow or ice pellets'
        elif item == '24': self.weather_decoded = 'Freezing drizzle or freezing rain'
        elif item == '25': self.weather_decoded = 'Shower(s) of rain'
        elif item == '26': self.weather_decoded = 'Shower(s) of snow, or of rain and snow'
        elif item == '27': self.weather_decoded = 'Shower(s) of hail, or of rain and hail'
        elif item == '28': self.weather_decoded = 'Fog or ice fog'
        elif item == '29': self.weather_decoded = 'Thunderstorm (with or withour precipitaion)'
        elif item == '30': self.weather_decoded = 'Slight or moderate duststorm or sandstorm has decreased during the preceding hour'
        elif item == '31': self.weather_decoded = 'Slight or moderate duststorm or sandstorm no appreciable change during the preceding hour'
        elif item == '32': self.weather_decoded = 'Slight or moderate duststorm or sandstorm has begun or has increased during the preceding hour'
        elif item == '33': self.weather_decoded = 'Severe duststorm or sandstorm has decreased during the preceding hour'
        elif item == '34': self.weather_decoded = 'Severe duststorm or sandstorm no appreciable change during the preceding hour'
        elif item == '35': self.weather_decoded = 'Severe duststorm or sandstorm has begun or has increased during the preceding hour'
        elif item == '36': self.weather_decoded = 'Slight or moderate drifting snow generally low'
        elif item == '37': self.weather_decoded = 'Heavy drifting snow generally low'
        elif item == '38': self.weather_decoded = 'Slight or moderate blowing snow generally high'
        elif item == '39': self.weather_decoded = 'Heavy blowing snow generally high'
        elif item == '40': self.weather_decoded = 'Fog or ice fog at a distance at the time of observation, but not at the station during the preceding hour, the fog or ice fog extending to a level above that of the observer'
        elif item == '41': self.weather_decoded = 'Fog or ice fog in patches'
        elif item == '42': self.weather_decoded = 'Fog or ice fog, sky visible has become thinner during the preceding hour'
        elif item == '43': self.weather_decoded = 'Fog or ice fog, sky invisible has become thinner during the preceding hour'
        elif item == '44': self.weather_decoded = 'Fog or ice fog, sky visible no appreciable change during the preceding hour'
        elif item == '45': self.weather_decoded = 'Fog or ice fog, sky invisible no appreciable change during the preceding hour'
        elif item == '46': self.weather_decoded = 'Fog or ice fog, sky visible has begun or has become thicker during the preceding hour'
        elif item == '47': self.weather_decoded = 'Fog or ice fog, sky visible has begun or has become thicker during the preceding hour'
        elif item == '48': self.weather_decoded = 'Fog, depositing rime, sky visible'
        elif item == '49': self.weather_decoded = 'Fog, depositing rime, sky invisible'
        elif item == '50': self.weather_decoded = 'Drizzle, not freezing, intermittent slight at time of observation'
        elif item == '51': self.weather_decoded = 'Drizzle, not freezing, continuous slight at time of observation'
        elif item == '52': self.weather_decoded = 'Drizzle, not freezing, intermittent moderate at time of observation'
        elif item == '53': self.weather_decoded = 'Drizzle, not freezing, continuous moderate at time of observation'
        elif item == '54': self.weather_decoded = 'Drizzle, not freezing, intermittent heavy (dense) at time of observation'
        elif item == '55': self.weather_decoded = 'Drizzle, not freezing, continuous heavy (dense) at time of observation'
        elif item == '56': self.weather_decoded = 'Drizzle, freezing, slight'
        elif item == '57': self.weather_decoded = 'Drizzle, freezing, moderate or heavy (dense)'
        elif item == '58': self.weather_decoded = 'Drizzle and rain, slight'
        elif item == '59': self.weather_decoded = 'Drizzle and rain, moderate or heavy'
        elif item == '60': self.weather_decoded = 'Rain, not freezing, intermittent slight at time of observation'
        elif item == '61': self.weather_decoded = 'Rain, not freezing, continuous slight at time of observation'
        elif item == '62': self.weather_decoded = 'Rain, not freezing, intermittent moderate at time of observation'
        elif item == '63': self.weather_decoded = 'Rain, not freezing, continuous moderate at time of observation'
        elif item == '64': self.weather_decoded = 'Rain, not freezing, intermittent heavy at time of observation'
        elif item == '65': self.weather_decoded = 'Rain, not freezing, continuous heavy at time of observation'
        elif item == '66': self.weather_decoded = 'Rain, freezing, slight'
        elif item == '67': self.weather_decoded = 'Rain, freezing, moderate or heavy'
        elif item == '68': self.weather_decoded = 'Rain, or drizzle and snow, slight'
        elif item == '69': self.weather_decoded = 'Rain, or drizzle and snow, moderate or heavy'
        elif item == '70': self.weather_decoded = 'Intermittent fall of snowflakes slight at time of observation'
        elif item == '71': self.weather_decoded = 'Continuous fall of snowflakes slight at time of observation'
        elif item == '72': self.weather_decoded = 'Intermittent fall of snowflakes moderate at time of observation'
        elif item == '73': self.weather_decoded = 'Continuous fall of snowflakes moderate at time of observation'
        elif item == '74': self.weather_decoded = 'Intermittent fall of snowflakes heavy at time of observation'
        elif item == '75': self.weather_decoded = 'Continuous fall of snowflakes heavy at time of observation'
        elif item == '76': self.weather_decoded = 'Diamond dust (without or without fog)'
        elif item == '77': self.weather_decoded = 'Snow grains (without or without fog)'
        elif item == '78': self.weather_decoded = 'Isolated star-like snow crystals (without or without fog)'
        elif item == '79': self.weather_decoded = 'Ice pellets'
        elif item == '80': self.weather_decoded = 'Rain shower(s), slight'
        elif item == '81': self.weather_decoded = 'Rain shower(s), moderate or heavy'
        elif item == '82': self.weather_decoded = 'Rain shower(s), violent'
        elif item == '83': self.weather_decoded = 'Shower(s) of rain and snow, mixed, slight'
        elif item == '84': self.weather_decoded = 'Shower(s) of rain and snow, mixed, moderate or heavy'
        elif item == '85': self.weather_decoded = 'Snow shower(s), slight'
        elif item == '86': self.weather_decoded = 'Snow shower(s), moderate or heavy'
        elif item == '87': self.weather_decoded = 'Shower(s) of snow pellets or small hail, with or without rain or rain and snow mixed slight'
        elif item == '88': self.weather_decoded = 'Shower(s) of snow pellets or small hail, with or without rain or rain and snow mixed moderate or heavy'
        elif item == '89': self.weather_decoded = 'Shower(s) of hail with or without rain or rain and snow mixed not associated with thunder slight'
        elif item == '90': self.weather_decoded = 'Shower(s) of hail with or without rain or rain and snow mixed not associated with thunder moderate or heavy'
        elif item == '91': self.weather_decoded = 'Slight rain at time of observation'
        elif item == '92': self.weather_decoded = 'Moderate or heavy rain at time of observation'
        elif item == '93': self.weather_decoded = 'Slight snow, or rain and snow mixed or hail at time of observation'
        elif item == '94': self.weather_decoded = 'Moderate or heavy snow, or rain and snow mixed or hail*** at time of observation'
        elif item == '95': self.weather_decoded = 'Thunderstorm, slight or moderate, without hail, but with rain and/or snow at time of observation'
        elif item == '96': self.weather_decoded = 'Thunderstorm, slight or moderate, with hail at time of observation'
        elif item == '97': self.weather_decoded = 'Thunderstorm, heavy, without hail, but with rain and/or snow at time of observation'
        elif item == '98': self.weather_decoded = 'Thunderstorm combined with duststorm or sandstorm at time of observation'
        elif item == '99': self.weather_decoded = 'Thunderstorm, heavy, with hail at time of observation'
        return True

    def generatePopupContent(self):
        data = '<div>'+self.message +'</div>'
        data += '<table id="tbl_warep" border="0" cellpadding="0" cellspacing="1">' # style="font-size: 11px!important;
        data += '<tr><td>Station</td><td>' + self.station + '</td></tr>'
        data += '<tr><td>Date</td><td>' +self.datetime_decode+ '</td></tr>'
        data += '<tr><td>Type</td><td>' +self.type+ '</td></tr>'
        data += '<tr><td>Index</td><td>' + self.index + '</td></tr>'
        data += '<tr><td>Wind</td><td>' + self.wind_decoded + '</td></tr>'
        data += '<tr><td>Cloud</td><td>' + self.cloud_decoded + '</td></tr>'
        data += '<tr><td>Visibility</td><td>' + self.visibility_decoded + '</td></tr>'
        data += '<tr><td>Precipitation</td><td>' + self.precipitation_decoded + '</td></tr>'
        data += '<tr><td>Deposits</td><td>' + self.deposits_decoded + '</td></tr>'
        data += '<tr><td>Weather</td><td>' + self.weather_decoded + '</td></tr>'
        data += '<tr><td>Hail</td><td>' + self.hail_decoded + '</td></tr>'
        data += '<tr><td>Mount</td><td>' + self.mounts_decoded + '</td></tr>'
        data += '</table>'
        return data