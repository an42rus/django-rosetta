from django.conf.urls import url
from django.contrib import admin

try:
    from django.urls import reverse_lazy
except:
    from django.core.urlresolvers import reverse_lazy

from django.views.generic import RedirectView

from rosetta.models import TranslationBackup, TranslationProxy
from rosetta.conf import settings as rosetta_settings
from rosetta.signals import reload_server


def restore(modeladmin, request, queryset):
    for backup in queryset:
        backup.restore()

    if rosetta_settings.AUTO_RELOAD:
        reload_server.send(sender=None, request=request)


class TranslationBackupAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions = [restore]
    save_on_top = True
    fields = ('created', 'locale_path', 'language', 'domain', 'content')
    list_display = ('created', 'locale_path', 'language', 'domain')
    list_filter = ('created', 'language', 'domain')
    readonly_fields = ('created', 'locale_path', 'language', 'domain')

    def has_add_permission(self, request):
        return False


class TranslationsAdmin(admin.ModelAdmin):
    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(
                r'^$',
                RedirectView.as_view(url=reverse_lazy('rosetta-pick-file')),
                name='%s_%s_changelist' % info
            ),
        ]
        return urlpatterns


admin.site.register(TranslationBackup, TranslationBackupAdmin)

if rosetta_settings.SHOW_AT_ADMIN_PANEL:
    admin.site.register(TranslationProxy, TranslationsAdmin)
