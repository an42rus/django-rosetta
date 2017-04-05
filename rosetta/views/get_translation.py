from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.generic.base import View

from rosetta.angular_translation_storage import get_translations_storage


class GetTranslationView(View):
    """
    get translations in selected language in json
    """

    http_method_names = ['get', ]

    def get(self, request, language, format=None):
        """
        Return a list of all translations for selected language.
        """
        available_languages = [l[0] for l in settings.LANGUAGES]

        if language not in available_languages:
            raise Http404()

        translation_storage = get_translations_storage()
        result = translation_storage.get(language)
        return HttpResponse(result)
