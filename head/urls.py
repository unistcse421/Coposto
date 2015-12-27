from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^city/$', views.city_search),
    url(r'^send_form_view$', views.send_form_view),
    url(r'^send_form_result.html$', views.send_form_result),
]