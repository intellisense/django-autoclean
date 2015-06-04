__author__ = 'Aamir'

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_noop as _

from .fields import AutoCleanField
from .util import clean


def base_clean_model(**kwargs):
    defaults = {
        'depends_on': 'name',
        'unique': True,
        'truncate_symbols': True,
    }
    defaults.update(kwargs)

    class WrapBaseCleanModel(models.Model):
        clean_key = AutoCleanField(**defaults)

        class Meta:
            abstract = True

        def clean(self):
            if defaults['unique']is True:
                value = getattr(self, defaults['depends_on'])
                new = self.pk is None
                qs = self._default_manager.all()
                if self.pk is not None:
                    qs = qs.exclude(pk=self.pk)
                if value and qs.filter(clean_key=clean(value, truncate_symbols=defaults['truncate_symbols']))\
                        .exists():
                    raise ValidationError(_('{0} with name "{1}" already exists.'.format(self.__class__.__name__, value)))

    return WrapBaseCleanModel

BaseCleanModel = base_clean_model()
