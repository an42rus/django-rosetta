from django.conf.urls import url
from .views import GetTranslationView

urlpatterns = [
    url(r'^(?P<language>[\w-]+)/$', GetTranslationView.as_view(), name='get_translations'),
]
