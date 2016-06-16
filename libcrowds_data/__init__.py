# -*- coding: utf8 -*-
"""
LibCrowdsData
-------------

Global data repository page for LibCrowds.
"""

import os
import json
import default_settings
from flask import current_app as app
from flask.ext.plugins import Plugin

__plugin__ = "LibCrowdsData"
__version__ =  json.load(open(os.path.join(os.path.dirname(__file__),
                                           'info.json')))['version']


class LibCrowdsData(Plugin):
    """Libcrowds data plugin class."""

    def setup(self):
        """Setup the plugin."""
        self.load_config()
        self.setup_blueprint()

    def load_config(self):
        """Configure the plugin."""
        settings = [key for key in dir(default_settings) if key.isupper()]
        for s in settings:
            if not app.config.get(s):
                app.config[s] = getattr(default_settings, s)

    def setup_blueprint(self):
        """Setup blueprint."""
        from .blueprint import DataBlueprint
        here = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(here, 'templates')
        static_folder = os.path.join(here, 'static')
        blueprint = DataBlueprint(template_folder=template_folder,
                                  static_folder=static_folder)
        app.register_blueprint(blueprint, url_prefix="/data")
