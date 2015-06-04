__author__ = 'Aamir'

from django.db.models import CharField
from django.utils.translation import ugettext_noop as _
from django.core.exceptions import FieldDoesNotExist
from django.core import checks

from .managers import AutoCleanManager
from .util import clean


class AutoCleanField(CharField):
    """
    A lower case char field which is dependent on another field value
    This field is helpful for unique lookup e.g. in get_or_create
    """

    def __init__(self, depends_on=None, manager_name='objects', truncate_symbols=True, *args, **kwargs):
        class_name = self.__class__.__name__

        if 'editable' in kwargs:
            raise TypeError(_('{0} can\'t have a editable constraints. This is automatically set.'
                              .format(class_name)))
        elif not depends_on:
            raise TypeError(_('{0} required a keyword parameter `depends_on` for which this field is bound.'
                              .format(class_name)))
        elif not isinstance(depends_on, basestring):
            raise TypeError(_('{0} `depends_on` parameter value should be a string (field name).'
                              .format(class_name)))

        self.depends_on = depends_on
        self.manager_name = manager_name
        self.truncate_symbols = truncate_symbols
        kwargs['max_length'] = kwargs.get('max_length', 255)
        kwargs['editable'] = False

        # Set db_index=True unless it's been set manually.
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True

        super(AutoCleanField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super(AutoCleanField, self).check(**kwargs)
        errors.extend(self._check_depends_on_field())
        return errors

    def _check_depends_on_field(self):
        try:
            field = self.model._meta.get_field(self.depends_on)
        except FieldDoesNotExist:
            error = _('{0} `depends_on` field "{1}" does not exists in model "{2}".'
                      .format(self.__class__.__name__, self.depends_on, self.model.__name__))
            return [
                checks.Error(error, hint=None, obj=self, id='AutoCleanField.E001', )
            ]
        else:
            if not isinstance(field, CharField):
                error = _('{0} `depends_on` field "{1}" should be an instance of '
                          'models.CharField.'
                          .format(self.__class__.__name__, self.depends_on))
                return [
                    checks.Error(error, hint=None, obj=self, id='AutoCleanField.E002', )
                ]
        return []

    def deconstruct(self):
        name, path, args, kwargs = super(AutoCleanField, self).deconstruct()

        if self.max_length != 255:
            kwargs.pop('max_length')

        if self.depends_on:
            kwargs['depends_on'] = self.depends_on

        if self.manager_name != 'objects':
            kwargs['manager_name'] = self.manager_name

        if self.truncate_symbols is not True:
            kwargs['truncate_symbols'] = self.truncate_symbols

        del kwargs['editable']

        kwargs.pop('db_index', None)

        return name, path, args, kwargs

    def contribute_to_class(self, cls, name):
        super(AutoCleanField, self).contribute_to_class(cls, name)
        cls.add_to_class(self.manager_name, AutoCleanManager())

    def pre_save(self, instance, add):
        # auto populate
        refined_value = None
        value = getattr(instance, self.depends_on)

        if value:
            refined_value = clean(value, truncate_symbols=self.truncate_symbols)

        if not self.blank:
            assert refined_value, 'Not able to generate auto value for field "{0}" having value "{1}"'\
                .format(self.depends_on, str(value))

        # make the updated refined_value available as instance attribute
        setattr(instance, self.name, refined_value)

        return refined_value
