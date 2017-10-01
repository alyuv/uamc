from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from mbr.views import *

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='mbr/home.html'), name='mbr_home'),
    url(r'^login/', auth_views.login, kwargs={'template_name': 'mbr/home.html'}, name='login'),
    url(r'^logout/', auth_views.logout, kwargs={'template_name': 'mbr/home.html'}, name='logout'),
    url(r'^contacts/', TemplateView.as_view(template_name='mbr/contacts.html'), name='contacts'),
]

# Get info
urlpatterns += [
    url(r'^flightdata/', FlightData.as_view(), name='mbr_flight_data'),
    #MRL Animations
    url(r'^mrl_j_animation/', ListMRL.as_view(), name='mbr_mrl_j_animation'),
    url(r'^mrl_h_animation/', ListMRL.as_view(level='H'), name='mbr_mrl_h_animation'),
    #Wareps
    url(r'^warep/', Warep.as_view(), name='warep'),
    url(r'^view_map/(?P<pk>\d+)/$', ViewBaseMap.as_view(), name='view_map'),
    url(r'^view_grib/(?P<pk>\d+)/$', ViewGRIB.as_view(), name='view_grib'),
    url(r'^view_sigwx/(?P<pk>\d+)/$', ViewSIGWX.as_view(), name='view_sigwx'),
    url(r'^view_mrl/(?P<pk>\d+)/$', ViewMRL.as_view(), name='view_mrl'),
    url(r'^view_pyua98/(?P<pk>\d+)/$', ViewPYUA98.as_view(), name='view_pyua98'),
    url(r'^view_qava91/(?P<pk>\d+)/$', ViewQAVA91.as_view(), name='view_qava91'),
    url(r'^volcanic_chart/(?P<pk>\d+)/$', ViewVolcanicAshImg.as_view(), name='view_volcanic_chart'),
]

#  Fly list management
urlpatterns += [
    url(r'^flight_list/', FlightList.as_view(), name='mbr_flight_list'),
    url(r'^add_flight/', AddFlight.as_view(), name='mbr_add_flight'),
    url(r'^update_flight/(?P<pk>\d+)/$', UpdateFlight.as_view(), name='mbr_update_flight'),
    url(r'^delete_flight/(?P<pk>\d+)/$', DeleteFlight.as_view(), name='mbr_delete_flight'),
]

#  Log management
urlpatterns += [
    url(r'^log_request/', ViewMbrLog.as_view(), name='mbr_set_log_request'),
]
