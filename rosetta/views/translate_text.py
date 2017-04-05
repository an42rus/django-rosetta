import json

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from microsofttranslator import Translator, TranslateApiException

from rosetta.access import can_translate


@user_passes_test(lambda user: can_translate(user), settings.LOGIN_URL)
def translate_text(request):
    language_from = request.GET.get('from', None)
    language_to = request.GET.get('to', None)
    text = request.GET.get('text', None)

    if language_from == language_to:
        data = {'success': True, 'translation': text}
    else:
        # run the translation:

        AZURE_CLIENT_ID = getattr(settings, 'AZURE_CLIENT_ID', None)
        AZURE_CLIENT_SECRET = getattr(settings, 'AZURE_CLIENT_SECRET', None)

        translator = Translator(AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)

        try:
            translated_text = translator.translate(text, language_to, language_from)
            data = {'success': True, 'translation': translated_text}
        except TranslateApiException as e:
            data = {'success': False, 'error': "Translation API Exception: {0}".format(e.message)}

    return HttpResponse(json.dumps(data), content_type='application/json')
