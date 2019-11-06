import hashlib
import os

import six
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import never_cache
from polib import pofile

from rosetta.access import can_translate, can_translate_language
from rosetta.poutil import find_pos
from rosetta.storage import get_storage
from rosetta.utils import get_app_name


@never_cache
@user_passes_test(lambda user: can_translate(user), settings.LOGIN_URL)
def lang_sel(request, langid, idx):
    """
    Selects a file to be translated
    """
    storage = get_storage(request)
    if langid not in [l[0] for l in settings.LANGUAGES] or not can_translate_language(request.user, langid):
        raise Http404
    else:

        rosetta_i18n_catalog_filter = storage.get('rosetta_i18n_catalog_filter', 'project')

        third_party_apps = rosetta_i18n_catalog_filter in ('all', 'third-party')
        django_apps = rosetta_i18n_catalog_filter in ('all', 'django')
        project_apps = rosetta_i18n_catalog_filter in ('all', 'project')
        file_ = sorted(find_pos(langid, project_apps=project_apps, django_apps=django_apps, third_party_apps=third_party_apps), key=get_app_name)[int(idx)]

        storage.set('rosetta_i18n_lang_code', langid)
        storage.set('rosetta_i18n_lang_name', six.text_type([l[1] for l in settings.LANGUAGES if l[0] == langid][0]))
        storage.set('rosetta_i18n_fn', file_)
        po = pofile(file_)
        for entry in po:
            entry.md5hash = hashlib.new(
                'md5',
                (six.text_type(entry.msgid) +
                    six.text_type(entry.msgstr) +
                    six.text_type(entry.msgctxt or "")).encode('utf8')
            ).hexdigest()

        storage.set('rosetta_i18n_pofile', po)
        try:
            os.utime(file_, None)
            storage.set('rosetta_i18n_write', True)
        except OSError:
            storage.set('rosetta_i18n_write', False)

        return HttpResponseRedirect(reverse('rosetta-home'))
