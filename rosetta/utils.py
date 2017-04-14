import json
import polib

from rosetta.angular_translation_storage import get_translations_storage


def convert(po_file, lang_code, encoding=None, pretty_print=False):
    if encoding is None:
        po = polib.pofile(po_file,
                          autodetect_encoding=True)
    else:
        po = polib.pofile(po_file,
                          autodetect_encoding=False,
                          encoding=encoding)

    data = {entry.msgid: entry.msgstr for entry in po if not entry.obsolete}
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