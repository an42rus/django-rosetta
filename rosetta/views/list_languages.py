import os

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from polib import pofile

import rosetta
from rosetta.access import can_translate, can_translate_language
from rosetta.conf import settings as rosetta_settings
from rosetta.poutil import find_pos
from rosetta.storage import get_storage
from rosetta.utils import get_app_name


@never_cache
@user_passes_test(lambda user: can_translate(user), settings.LOGIN_URL)
def list_languages(request, do_session_warn=False):
    """
    Lists the languages for the current project, the gettext catalog files
    that can be translated and their translation progress
    """
    storage = get_storage(request)
    languages = []

    if 'filter' in request.GET:
        if request.GET.get('filter') in ('project', 'third-party', 'django', 'all'):
            filter_ = request.GET.get('filter')
            storage.set('rosetta_i18n_catalog_filter', filter_)
            return HttpResponseRedirect(reverse('rosetta-pick-file'))

    rosetta_i18n_catalog_filter = storage.get('rosetta_i18n_catalog_filter', 'project')

    third_party_apps = rosetta_i18n_catalog_filter in ('all', 'third-party')
    django_apps = rosetta_i18n_catalog_filter in ('all', 'django')
    project_apps = rosetta_i18n_catalog_filter in ('all', 'project')

    has_pos = False
    for language in settings.LANGUAGES:
        if not can_translate_language(request.user, language[0]):
            continue

        pos = find_pos(language[0], project_apps=project_apps, django_apps=django_apps, third_party_apps=third_party_apps)
        has_pos = has_pos or len(pos)
        languages.append(
            (
                language[0],
                _(language[1]),
                sorted([(get_app_name(l), os.path.realpath(l), pofile(l)) for l in pos], key=lambda app: app[0]),
            )
        )
    try:
        ADMIN_MEDIA_PREFIX = settings.ADMIN_MEDIA_PREFIX
    except AttributeError:
        ADMIN_MEDIA_PREFIX = settings.STATIC_URL + 'admin/'
    do_session_warn = do_session_warn and 'SessionRosettaStorage' in rosetta_settings.STORAGE_CLASS and 'signed_cookies' in settings.SESSION_ENGINE

    return render(request, 'rosetta/languages.html', dict(
        version=rosetta.get_version(True),
        ADMIN_MEDIA_PREFIX=ADMIN_MEDIA_PREFIX,
        do_session_warn=do_session_warn,
        languages=languages,
        has_pos=has_pos,
        rosetta_i18n_catalog_filter=rosetta_i18n_catalog_filter
    ))
