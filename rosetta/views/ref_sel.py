from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import never_cache

from rosetta.access import can_translate
from rosetta.storage import get_storage


def ref_sel(request, langid):
    storage = get_storage(request)
    ALLOWED_LANGUAGES = [l[0] for l in settings.LANGUAGES] + ['msgid']

    if langid not in ALLOWED_LANGUAGES:
        raise Http404

    storage.set('rosetta_i18n_ref_lang_code', langid)

    return HttpResponseRedirect(reverse('rosetta-home'))
ref_sel = never_cache(ref_sel)
ref_sel = user_passes_test(lambda user: can_translate(user), settings.LOGIN_URL)(ref_sel)
