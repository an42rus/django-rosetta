from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^api/translations/', include('rosetta.urls_api'))
]

urlpatterns += staticfiles_urlpatterns()
