from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    url(r'^', include('head.urls')),
    url(r'^admin/', admin.site.urls),
]
