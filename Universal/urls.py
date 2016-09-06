from django.conf.urls import url
from Universal import views

urlpatterns = [
    url(r'^CarInfo/(?P<pk>[0-9]+)/$', views.cardetails),
    url(r'^UserSignUp/$', views.usersignup),
    url(r'^addr/(?P<pk>[0-9]+)/$', views.address),
    #url(r'^request/(?P<pk>[0-9]+)/$', views.initiate_request),
    url(r'^slotscheck/(?P<pk>[0-9]+)/$', views.findSlotsForDate),
    url(r'^request/(?P<pk>[0-9]+)/$', views.initreq),
    url(r'^requestatusinfo/(?P<pk>[0-9]+)/$',views.requeststatus_info),
    url(r'^driver_jobs/(?P<pk>[0-9]+)/$',views.driverjobdetails),
    url(r'^feedback/(?P<pk>[0-9]+)/$',views.submitfeedback),
    url(r'^requestcancel/(?P<pk>[0-9]+)/$',views.cancelrequest),
    url(r'^userrequests/(?P<pk>[0-9]+)/$',views.getuserrequests),
    url(r'^changedriver/(?P<pk>[0-9]+)/$',views.changedriver),
    url(r'^locationservices/(?P<pk>[0-9]+)/$',views.locationbasedServices),
    url(r'^services_version/(?P<pk>[0-9]+)/$',views.serviceversion),
    url(r'^getcars/(?P<pk>[0-9]+)/$',views.modelsandbrands),
    url(r'^getjointdriver/(?P<pk>[0-9]+)/$',views.getjointdrivers)

]
