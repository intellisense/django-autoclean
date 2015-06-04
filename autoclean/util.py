# -*- coding: utf-8 -*-

__author__ = 'Aamir'


def clean(value, truncate_symbols=True):
    """

    :param value: basestring
    :param truncate_symbols: whether to truncate symbols from string
    :return: lowercase cleaned string based, alpha numeric characters if truncate_symbols=True
    """
    if value:
        parts = [v.lower() for v in list(value.strip())]
        if truncate_symbols:
            parts[:] = [v for v in parts if v.isalpha() or v.isdigit()]
        value = ''.join(parts)
    return value
