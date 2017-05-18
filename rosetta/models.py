import os

import polib
from django.db import models
from django.utils.translation import ugettext as _

from rosetta.utils import put_translation_to_storage


class TranslationBackup(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    language = models.CharField(db_index=True, max_length=5)
    locale_path = models.CharField(db_index=True, max_length=256)
    domain = models.CharField(db_index=True, max_length=256)

    content = models.TextField()

    class Meta:
        ordering = ('-created',)

    def restore(self):
        po_filename = os.path.join(
            self.locale_path,
            self.language,
            'LC_MESSAGES',
            self.domain + '.po'
        )

        mo_filename = os.path.join(
            self.locale_path,
            self.language,
            'LC_MESSAGES',
            self.domain + '.mo'
        )

        with open(po_filename, 'w') as output:
            output.write(self.content)

        po = polib.pofile(po_filename)
        po.save_as_mofile(mo_filename)

        if self.domain == 'angular':
            put_translation_to_storage(self.language, po_filename)

    def __unicode__(self):
        return "(%s:%s:%s)" % (self.pk, self.language, self.locale_path)

    def __str__(self):
        return "(%s:%s:%s)" % (self.pk, self.language, self.locale_path)


class TranslationProxy(TranslationBackup):
    """
     Small hook to add item to admin interface under the same app name
    """

    class Meta:
        verbose_name = _('Translation')
        proxy = True
