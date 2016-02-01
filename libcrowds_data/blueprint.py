# -*- coding: utf8 -*-
"""Blueprint module for libcrowds-data."""

from flask import Blueprint
from .view import index


class DataBlueprint(Blueprint):
    """Blueprint to support additional views.

    :param ``**kwargs``: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        defaults = {'name': 'data', 'import_name': __name__}
        defaults.update(kwargs)

        super(StatisticsBlueprint, self).__init__(**defaults)

        self.add_url_rule("/", view_func=index)
