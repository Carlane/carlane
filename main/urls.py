from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^new', views.home_new),
    url(r'^', views.home)
]
