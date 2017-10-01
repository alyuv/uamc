from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, User


class Airline(models.Model):
    iata = models.CharField(max_length=2, null=True, blank=True)
    icao = models.CharField(max_length=4, null=True, blank=True)
    name_uk = models.CharField(max_length=100, unique=True)
    name_en = models.CharField(max_length=100, unique=True)
    name_ru = models.CharField(max_length=100, unique=True)
    comments = models.CharField(max_length=100, blank=True)
    auth_group = models.ForeignKey(Group, models.DO_NOTHING)

    class Meta:
        db_table = 'airline'
        permissions = (
            ('can_view_mbr_info', 'can get mbr info in html format'),
        )

    def __str__(self):
        return self.name_uk


class FlightTable(models.Model):
    airline = models.ForeignKey(Airline, models.DO_NOTHING)
    number = models.CharField(max_length=10, blank=True, null=True)
    airport_from = models.CharField(max_length=4)
    airport_to = models.CharField(max_length=4)
    alt_airport = models.CharField(max_length=100, blank=True, null=True)

    departure_time = models.TimeField()
    flight_duration = models.TimeField()

    firs = models.CharField(max_length=100, blank=True, null=True)

    level450 = models.BooleanField(default=False)
    level410 = models.BooleanField(default=False)
    level390 = models.BooleanField(default=False)
    level360 = models.BooleanField(default=False)
    level340 = models.BooleanField(default=False)
    level320 = models.BooleanField(default=False)
    level300 = models.BooleanField(default=False)
    level270 = models.BooleanField(default=False)
    level240 = models.BooleanField(default=False)
    level180 = models.BooleanField(default=False)
    level140 = models.BooleanField(default=False)
    level100 = models.BooleanField(default=False)
    level050 = models.BooleanField(default=False)

    region_c = models.BooleanField(default=False)
    region_g = models.BooleanField(default=False)
    region_h = models.BooleanField(default=False)
    region_eur = models.BooleanField(default=False)
    region_mid = models.BooleanField(default=False)
    region_sasia = models.BooleanField(default=False)

    airmet = models.BooleanField(default=False)
    gamet = models.BooleanField(default=False)
    volcanic_ash = models.BooleanField(default=False)

    def __str__(self):
        return 'From {} to {} at {}'.format(self.airport_from, self.airport_to,
                                            self.departure_time)

    class Meta:
        db_table = 'flight_table'


class MbrLog(models.Model):
    actiondate = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, models.DO_NOTHING)
    operation = models.CharField(max_length=50)
    result = models.TextField()
    request = models.TextField()

    class Meta:
        db_table = 'mbr_log'


class IcaoStation(models.Model):
    station_index = models.CharField(unique=True, max_length=4)
    archive = models.BooleanField(default=False)

    class Meta:
        app_label = 'meteodata'
        managed = False
        db_table = 'icao_station'


class NumericStation(models.Model):
    station_index = models.IntegerField(unique=True)
    name_en = models.CharField(max_length=40, db_column='name_en-GB')
    name_uk = models.CharField(max_length=40, db_column='name_uk-UA')
    name_ru = models.CharField(max_length=40, db_column='name_ru-RU')
    lon = models.DecimalField(max_digits=6, decimal_places=4)
    lat = models.DecimalField(max_digits=6, decimal_places=4)
    fir = models.CharField(max_length=4)

    class Meta:
        app_label = 'meteodata'
        managed = False
        db_table = 'numeric_station'


class Message(models.Model):
    message = models.TextField()
    valid_begin = models.DateTimeField()
    valid_end = models.DateTimeField()
    channel = models.CharField(max_length=20)
    channel_time = models.DateTimeField()
    gts_yygggg = models.CharField(max_length=6, null=False)
    gts_bbb = models.CharField(max_length=3, blank=True)
    insert_time = models.DateTimeField()
    hash = models.UUIDField(unique=True)

    class Meta:
        abstract = True
        managed = False


class MessageIcaoStation(Message):
    station = models.ForeignKey(IcaoStation, models.DO_NOTHING)

    class Meta:
        abstract = True


class METAR(MessageIcaoStation):
    """ METAR and SPECI """
    class Meta:
        app_label = 'meteodata'
        db_table = 'metar'
        ordering = ['-valid_end']


class TAF(MessageIcaoStation):
    """ TAF """
    class Meta:
        app_label = 'meteodata'
        db_table = 'taf'


class SIGMET(MessageIcaoStation):
    """ SIGMET """
    class Meta:
        app_label = 'meteodata'
        db_table = 'sigmet'


class AIREP(MessageIcaoStation):
    """ SIGMET """
    class Meta:
        app_label = 'meteodata'
        db_table = 'airep'


class AIRMET(MessageIcaoStation):
    """ SIGMET """
    class Meta:
        app_label = 'meteodata'
        db_table = 'airmet'


class GAMET(MessageIcaoStation):
    """ SIGMET """
    class Meta:
        app_label = 'meteodata'
        db_table = 'gamet'


class WAREP(Message):
    station = models.ForeignKey(NumericStation, models.DO_NOTHING)

    class Meta:
        app_label = 'meteodata'
        db_table = 'warep'


class BaseMap(models.Model):
    file_name = models.TextField()
    in_base64 = models.TextField()
    file_ext = models.CharField(max_length=4)
    channel = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    valid_begin = models.DateTimeField()
    valid_end = models.DateTimeField()
    channel_time = models.DateTimeField()
    insert_time = models.DateTimeField()

    class Meta:
        abstract = True
        managed = False
        ordering = ['-valid_end']


class MRL(BaseMap):
    im_level = models.CharField(max_length=20)

    class Meta:
        app_label = 'meteodata'
        db_table = 'mrl_img'
        ordering = ['-valid_end']


class GRIB(BaseMap):
    im_level = models.CharField(max_length=20)
    source_time = models.DateTimeField()

    class Meta:
        app_label = 'meteodata'
        db_table = 'grib_img'


class SIGWX(BaseMap):
    im_level = models.CharField(max_length=20)
    source_time = models.DateTimeField()

    class Meta:
        app_label = 'meteodata'
        db_table = 'sigwx_img'


class PYUA98(BaseMap):

    class Meta:
        app_label = 'meteodata'
        db_table = 'pyua98_img'


class QAVA91(BaseMap):

    class Meta:
        app_label = 'meteodata'
        db_table = 'qava91_img'

class VolcanicAshImg(BaseMap):

    class Meta:
        app_label = 'meteodata'
        db_table = 'volcanic_img'
