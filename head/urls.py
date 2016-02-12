from django.conf.urls import url, include
from head.views import RegistrationViewUniqueEmail

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^city/$', views.city_search),
    url(r'^send_form_view$', views.send_form_view),
    url(r'^send_result/$', views.send_result),
    url(r'^bring_submit/$', views.bring_submit),
    url(r'^send_form_validator/$', views.send_form_validator),
    url(r'^reg_form_validator/$', views.reg_form_validator),
    url(r'^accounts/register/$', RegistrationViewUniqueEmail.as_view(), name='registration_register'),
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/reg_result/$', views.reg_result),
    url(r'^accounts/login_result/$', views.login_result),
    url(r'^accounts/account_view/$', views.account_view),
    url(r'^accounts/logout/$', views.logout),
    url(r'^accounts/send_list/$', views.user_send_list),
    url(r'^accounts/bring_list/$', views.user_bring_list),
    url(r'^bring_result/$', views.bring_result),
    url(r'^accounts/', include('registration.backends.hmac.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)