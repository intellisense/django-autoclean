__author__ = 'Aamir'

from django.db import models

from .util import clean


class AutoCleanQuerySet(models.QuerySet):
    def get_or_create(self, defaults=None, **kwargs):
        lookup, params = self._extract_model_params(defaults, **kwargs)
        custom_lookup = lookup.copy()
        for field in self.model._meta.fields:
            if hasattr(field, 'depends_on') and field.depends_on in lookup:
                custom_lookup[field.attname] = clean(custom_lookup.pop(field.depends_on),
                                                     truncate_symbols=field.truncate_symbols)

        self._for_write = True
        try:
            return self.get(**custom_lookup), False
        except self.model.DoesNotExist:
            return self._create_object_from_params(lookup, params)


class AutoCleanManager(models.Manager):
    def get_queryset(self):
        return AutoCleanQuerySet(self.model, using=self._db)
