from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    created_by = models.ForeignKey('general.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Created by'))
    updated_by = models.ForeignKey('general.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_updated', verbose_name=_('Updated by'))


    class Meta:
        abstract = True