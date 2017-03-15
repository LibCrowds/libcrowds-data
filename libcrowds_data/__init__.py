# -*- coding: utf8 -*-
"""
LibCrowdsData
-------------

Global data repository page for LibCrowds.
"""

import os
import json
from flask import current_app as app
from flask.ext.plugins import Plugin

__plugin__ = "LibCrowdsData"
__version__ = json.load(open(os.path.join(os.path.dirname(__file__),
                                          'info.json')))['version']


class LibCrowdsData(Plugin):
    """Libcrowds data plugin class."""

    def setup(self):
        """Setup the plugin."""
        self.setup_blueprint()

    def setup_blueprint(self):
        """Setup blueprint."""
        from .view import blueprint
        app.register_blueprint(blueprint, url_prefix="/data")
