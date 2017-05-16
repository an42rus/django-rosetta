import codecs
import json
import os
from glob import glob

import logging
import polib
from django.conf import settings

from rosetta.angular_translation_storage import get_translations_storage
from rosetta.models import TranslationBackup

logger = logging.getLogger()


def convert(po_file, lang_code, encoding=None, pretty_print=False):
    if encoding is None:
        po = polib.pofile(po_file,
                          autodetect_encoding=True)
    else:
        po = polib.pofile(po_file,
                          autodetect_encoding=False,
                          encoding=encoding)

    data = {entry.msgid: entry.msgstr for entry in po if entry.msgstr.strip() and not entry.obsolete}
    data = {lang_code: data}

    if not pretty_print:
        result = json.dumps(data, ensure_ascii=False, sort_keys=True)
    else:
        result = json.dumps(data, sort_keys=True, indent=4 * ' ',
                                  ensure_ascii=False)
    return result


def put_translation_to_storage(lang_code, po_path):
    result = convert(po_path, lang_code)
    translation_storage = get_translations_storage()
    translation_storage.set(lang_code, result)


def get_app_name(path):
    app = path.split("/locale")[0].split("/")[-1]
    return app


def backup_all_po_files_to_db():
    for lang, lang_name in settings.LANGUAGES:
        backup_po_to_db_by_language_and_domains(lang)


def backup_po_to_db_by_language_and_domains(language, domains=['django', 'djangojs', 'angular']):
    """ Backup Po file to db model by language"""

    available_langs = dict(settings.LANGUAGES)
    if language not in available_langs:
        logger.debug('Language %s is not available for backup. Add language to settings.LANGUAGES' % language)
        return

    for path in settings.LOCALE_PATHS:
        po_pattern = os.path.join(path, language, "LC_MESSAGES", "*.po")

        for pofile in glob(po_pattern):
            logger.debug("Backuping %s" % pofile)

            domain = os.path.splitext(os.path.basename(pofile))[0]
            if domain in domains:
                with codecs.open(pofile, 'r', 'utf-8') as pofile_opened:
                    content = pofile_opened.read()

                    backup = TranslationBackup(
                        language=language,
                        locale_path=path,
                        domain=domain,
                        content=content,
                    )
                    backup.save()
