from django.core.exceptions import ImproperlyConfigured

from rosetta.conf import settings as rosetta_settings

try:
    from django.core.cache import caches
    cache = caches[rosetta_settings.ROSETTA_CACHE_NAME]
except ImportError:
    from django.core.cache import get_cache
    cache = get_cache(rosetta_settings.ROSETTA_CACHE_NAME)

try:
    import importlib
except ImportError:
    from django.utils import importlib


class BaseAngularTranslationStorage(object):
    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, val):
        raise NotImplementedError

    def has(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError


class CacheAngularTranslationStorage(BaseAngularTranslationStorage):
    def __init__(self):
        # Make sure the cache actually works
        try:
            self.set('rosetta_cache_test', 'rosetta')
            if not self.get('rosetta_cache_test') == 'rosetta':
                raise ImproperlyConfigured("You can't use the CacheAngularTranslationStorage if your cache isn't correctly set up, please double check your Django DATABASES setting and that the cache server is responding.")
        finally:
            self.delete('rosetta_cache_test')

    def get(self, key, default=None):
        return cache.get(key, default)

    def set(self, key, val):
        cache.set(key, val, None)

    def has(self, key):
        return key in cache

    def delete(self, key):
        cache.delete(key)


def get_translations_storage():
    from rosetta.conf import settings
    storage_module, storage_class = settings.ANGULAR_TRANSLATION_STORAGE_CLASS.rsplit('.', 1)
    storage_module = importlib.import_module(storage_module)
    return getattr(storage_module, storage_class)()
