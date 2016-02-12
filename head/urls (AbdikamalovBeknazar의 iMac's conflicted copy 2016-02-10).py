from django.conf.urls import url, include
from head.views import RegistrationViewUniqueEmail

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^city/$', views.city_search),
    url(r'^send_form_view$', views.send_form_view),
    url(r'^send_form_result.html$', views.send_form_result),
    url(r'^send_form_validator/$', views.send_form_validator),
    url(r'^accounts/register/$', RegistrationViewUniqueEmail.as_view(), name='registration_register'),
    # url(r'^accounts/', include('registration.backends.hmac.urls'))
]