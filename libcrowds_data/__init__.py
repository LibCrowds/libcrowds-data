# -*- coding: utf8 -*-
"""
LibCrowdsData
-------------

Global data repository page for LibCrowds.
"""

import os
from flask import current_app as app
from flask.ext.plugins import Plugin

__plugin__ = "LibCrowdsData"
__version__ = "0.1.4"


class LibCrowdsData(Plugin):
    """Libcrowds data plugin class."""

    def setup(self):
        """Setup the plugin."""
        self.setup_blueprint()

    def setup_blueprint(self):
        """Setup blueprint."""
        from .blueprint import DataBlueprint
        here = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(here, 'templates')
        static_folder = os.path.join(here, 'static')
        blueprint = DataBlueprint(template_folder=template_folder,
                                  static_folder=static_folder)
        app.register_blueprint(blueprint, url_prefix="/data")
