from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$',views.register),
    url(r'^success$',views.success),
    url(r'^login$',views.login),
    url(r'^create$',views.create),
   url(r'^plan_process$',views.plan_process),
   url(r'^show/(?P<id>\d+)$',views.show),
   url(r'^remove/(?P<id>\d+)$',views.remove),

]