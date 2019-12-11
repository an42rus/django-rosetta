from __future__ import unicode_literals

import glob
import os

from django.core.management.base import CommandError
from django.core.management.commands.compilemessages import Command as OriginCommand
from django.core.management.commands.compilemessages import has_bom
from django.core.management.utils import find_command

from rosetta.conf import settings as rosetta_settings
from rosetta.utils import put_translation_to_storage


class Command(OriginCommand):
    def handle(self, **options):
        locale = options['locale']
        exclude = options['exclude']
        self.verbosity = options['verbosity']
        if options['fuzzy']:
            self.program_options = self.program_options + ['-f']

        if find_command(self.program) is None:
            raise CommandError("Can't find %s. Make sure you have GNU gettext "
                               "tools 0.15 or newer installed." % self.program)

        basedirs = [os.path.join('conf', 'locale'), 'locale']
        if os.environ.get('DJANGO_SETTINGS_MODULE'):
            from django.conf import settings
            basedirs.extend(path for path in settings.LOCALE_PATHS)

        # Walk entire tree, looking for locale directories
        for dirpath, dirnames, filenames in os.walk('.', topdown=True):
            for dirname in dirnames:
                if dirname == 'locale':
                    basedirs.append(os.path.join(dirpath, dirname))

        # Gather existing directories.
        basedirs = set(map(os.path.abspath, filter(os.path.isdir, basedirs)))

        if not basedirs:
            raise CommandError("This script should be run from the Django Git "
                               "checkout or your project or app tree, or with "
                               "the settings module specified.")

        # Build locale list
        all_locales = []
        for basedir in basedirs:
            locale_dirs = filter(os.path.isdir, glob.glob('%s/*' % basedir))
            all_locales.extend(map(os.path.basename, locale_dirs))

        # Account for excluded locales
        locales = locale or all_locales
        locales = set(locales) - set(exclude)

        if not locales:
            if self.verbosity > 0:
                self.stdout.write('Nothing to process. All available locales excluded')
            return

        for basedir in basedirs:
            for l in locales:
                if self.verbosity > 0:
                    self.stdout.write('processing locale %s\n' % l)
                ldir = os.path.join(basedir, l, 'LC_MESSAGES')

                locations = []
                for dirpath, dirnames, filenames in os.walk(ldir):
                    locations.extend((dirpath, f) for f in filenames if f.endswith('.po'))

                if not locations:
                    continue

                django_locations = filter(lambda x: x[1] in ['django.po', 'djangojs.po'], locations)
                django_locations = list(django_locations)
                self.compile_messages(django_locations)

                if rosetta_settings.ENABLE_ANGULAR_TRANSLATION:
                    angular_locations = filter(lambda x: x[1] == 'angular.po', locations)
                    angular_locations = list(angular_locations)

                    self.store_angular_translations(l, angular_locations)
                    self.compile_messages(angular_locations)

    def store_angular_translations(self, l, locations):
        """
        Locations is a list of tuples: [(directory, file), ...]
        """
        for i, (dirpath, f) in enumerate(locations):
            if self.verbosity > 0:
                self.stdout.write('processing file %s in %s\n' % (f, dirpath))
            po_path = os.path.join(dirpath, f)
            if has_bom(po_path):
                raise CommandError("The %s file has a BOM (Byte Order Mark). "
                                   "Django only supports .po files encoded in "
                                   "UTF-8 and without any BOM." % po_path)

            put_translation_to_storage(l, po_path)
