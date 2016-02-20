from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    url(r'^', include('head.urls')),
    #url(r'^head/', include('head.urls')),#changed by Alibek
    url(r'^api-auth/', include( 'rest_framework.urls', namespace='rest_framework' ) ),#changed by Alibek
  # url(r'^admin/', admin.site.urls),
]
