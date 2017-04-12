from __future__ import unicode_literals

import glob
import os
import io

import sys

from django.conf import settings
from django.core.management import CommandError
from django.core.management.utils import handle_extensions
from django.utils.text import get_text_list

from rosetta.conf import settings as rosetta_settings
from django.core.management.commands.makemessages import Command as OriginCommand
from django.core.management.commands.makemessages import check_programs


class Command(OriginCommand):
    help = (
        "Runs over the entire source tree of the current directory and "
        "pulls out all strings marked for translation. It creates (or updates) a message "
        "file in the conf/locale (in the django tree) or locale (for projects and "
        "applications) directory.\n\nYou must run this command with one of either the "
        "--locale, --exclude, or --all options."
    )

    def handle(self, *args, **options):
        locale = options['locale']
        exclude = options['exclude']
        self.domain = options['domain']
        self.verbosity = options['verbosity']
        process_all = options['all']
        extensions = options['extensions']
        self.symlinks = options['symlinks']

        # Need to ensure that the i18n framework is enabled
        if settings.configured:
            settings.USE_I18N = True
        else:
            settings.configure(USE_I18N=True)

        ignore_patterns = options['ignore_patterns']
        if options['use_default_ignore_patterns']:
            ignore_patterns += ['CVS', '.*', '*~', '*.pyc']
        self.ignore_patterns = list(set(ignore_patterns))

        # Avoid messing with mutable class variables
        if options['no_wrap']:
            self.msgmerge_options = self.msgmerge_options[:] + ['--no-wrap']
            self.msguniq_options = self.msguniq_options[:] + ['--no-wrap']
            self.msgattrib_options = self.msgattrib_options[:] + ['--no-wrap']
            self.xgettext_options = self.xgettext_options[:] + ['--no-wrap']
        if options['no_location']:
            self.msgmerge_options = self.msgmerge_options[:] + ['--no-location']
            self.msguniq_options = self.msguniq_options[:] + ['--no-location']
            self.msgattrib_options = self.msgattrib_options[:] + ['--no-location']
            self.xgettext_options = self.xgettext_options[:] + ['--no-location']

        self.no_obsolete = options['no_obsolete']
        self.keep_pot = options['keep_pot']

        if self.domain not in ('django', 'djangojs', 'angular'):
            raise CommandError("currently makemessages only supports domains "
                               "'django' and 'djangojs'")
        if self.domain == 'djangojs':
            exts = extensions if extensions else ['js']
        else:
            exts = extensions if extensions else ['html', 'txt', 'py']
        self.extensions = handle_extensions(exts)

        if (locale is None and not exclude and not process_all) or self.domain is None:
            raise CommandError(
                "Type '%s help %s' for usage information."
                % (os.path.basename(sys.argv[0]), sys.argv[1])
            )

        if self.verbosity > 1:
            self.stdout.write(
                'examining files with the extensions: %s\n'
                % get_text_list(list(self.extensions), 'and')
            )

        self.invoked_for_django = False
        self.locale_paths = []
        self.default_locale_path = None
        if os.path.isdir(os.path.join('conf', 'locale')):
            self.locale_paths = [os.path.abspath(os.path.join('conf', 'locale'))]
            self.default_locale_path = self.locale_paths[0]
            self.invoked_for_django = True
        else:
            self.locale_paths.extend(settings.LOCALE_PATHS)
            # Allow to run makemessages inside an app dir
            if os.path.isdir('locale'):
                self.locale_paths.append(os.path.abspath('locale'))
            if self.locale_paths:
                self.default_locale_path = self.locale_paths[0]
                if not os.path.exists(self.default_locale_path):
                    os.makedirs(self.default_locale_path)

        # Build locale list
        locale_dirs = filter(os.path.isdir, glob.glob('%s/*' % self.default_locale_path))
        all_locales = map(os.path.basename, locale_dirs)

        # Account for excluded locales
        if process_all:
            locales = all_locales
        else:
            locales = locale or all_locales
            locales = set(locales) - set(exclude)

        if locales:
            check_programs('msguniq', 'msgmerge', 'msgattrib')

        check_programs('xgettext')

        try:
            potfiles = self.build_potfiles()

            # Build po files for each selected locale
            for locale in locales:
                if self.verbosity > 0:
                    self.stdout.write("processing locale %s\n" % locale)
                for potfile in potfiles:
                    self.stdout.write("path %s\n" % potfile)
                    self.write_po_file(potfile, locale)
        finally:
            if not self.keep_pot:
                self.remove_potfiles()

    def copy_angular_potfile(self):
        angular_pot_path = os.path.join(rosetta_settings.ANGULAR_TRANSLATION_FILE_PATH)
        if os.path.exists(angular_pot_path):
            with io.open(angular_pot_path, 'r', encoding='utf-8') as fp:
                content = fp.read()

            for path in self.locale_paths:
                pot_path = os.path.join(path, '%s.pot' % str(self.domain))
                with io.open(pot_path, 'w', encoding='utf-8') as fp:
                    fp.write(content)

    def process_files(self, file_list):
        """
            build pot files
        """
        super(Command, self).process_files(file_list)

        if self.domain == 'angular' and rosetta_settings.ENABLE_ANGULAR_TRANSLATION:
            self.copy_angular_potfile()
