Angular translation Settings
============================

Rosetta can be configured via the following parameters, to be defined in your project settings file:

* ``ROSETTA_ENABLE_ANGULAR_TRANSLATION``: Enable translation for Angular files. Defaults to ``False``.
* ``ROSETTA_ANGULAR_TRANSLATION_FILE_PATH``: Path to Angular .pot file. Defaults to ````.
* ``ROSETTA_ANGULAR_TRANSLATION_STORAGE_CLASS``: See the note below on Storages. Defaults to ``rosetta.angular_translation_storage.CacheAngularTranslationStorage``

Angular translation Storages
----------------------------

To prevent re-reading and parsing the PO file catalogs over and over again to get Angular translations, Rosetta stores them in a volatile location. This can be either the Django cache or something else you want.

We use the Cache-based backend by default (``'rosetta.angular_translation_storage.CacheAngularTranslationStorage'``). Please make sure that a proper ``CACHES`` backend is configured in your Django settings if your Django app is being served in a multi-process environment, or the different server processes, serving subsequent requests, won't find the storage data left by previous requests.

Alternatively you can switch to using other storage by setting ``ROSETTA_ANGULAR_TRANSLATION_STORAGE_CLASS = 'path.to.your.storage'`` in your settings.

**TL;DR**: if you run Django with gunincorn, mod-wsgi or other multi-process environment, the Django-default ``CACHES`` ``LocMemCache`` backend won't suffice: use memcache instead, or you will run into issues.
