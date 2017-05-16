from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache

from rosetta.access import can_translate
from rosetta.storage import get_storage
from rosetta.utils import backup_po_to_db_by_language, backup_all_po_files_to_db


@never_cache
@user_passes_test(lambda user: can_translate(user), settings.LOGIN_URL)
def backup_file(request):

    backup_all_files = request.GET.get('all')
    if backup_all_files:
        backup_all_po_files_to_db()
        return HttpResponseRedirect(reverse('rosetta-pick-file'))

    storage = get_storage(request)
    # language code
    lang_code = storage.get('rosetta_i18n_lang_code', None)

    backup_po_to_db_by_language(lang_code)
    return HttpResponseRedirect(reverse('rosetta-home'))
