# -*- coding: utf8 -*-
"""Blueprint module for libcrowds-data."""

from flask import Blueprint
from .view import index, csv_export, xml_export


class DataBlueprint(Blueprint):
    """Blueprint to support additional views.

    :param ``**kwargs``: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        defaults = {'name': 'data', 'import_name': __name__}
        defaults.update(kwargs)
        super(DataBlueprint, self).__init__(**defaults)
        self.add_url_rule("/", view_func=index)
        self.add_url_rule("/<short_name>/csv_export", view_func=csv_export)
        self.add_url_rule("/<short_name>/xml_export", view_func=xml_export)
