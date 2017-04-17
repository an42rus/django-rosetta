from django.http import HttpResponse
from django.views.generic.base import View

from rosetta.conf import settings as rosetta_settings
from rosetta.signals import reload_server


class ReloadServerView(View):
    """
        Reload server manually
    """

    http_method_names = ['post', ]

    def post(self, request):
        if rosetta_settings.AUTO_RELOAD:
            return HttpResponse(status=400)

        reload_server.send(sender=None, request=request)
        return HttpResponse(status=200)
