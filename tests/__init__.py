# -*- coding: utf8 -*-

import sys
import os
import libcrowds_data as plugin


# Use the PyBossa test suite
sys.path.append(os.path.abspath("./pybossa/test"))

from default import with_context
from helper import web


def setUpPackage():
    """Setup the plugin."""
    from default import flask_app
    with flask_app.app_context():
        plugin_dir = os.path.dirname(plugin.__file__)
        plugin.LibCrowdsData(plugin_dir).setup()


class TestPlugin(web.Helper):


    def test_blueprint_registered(self):
        assert 'data' in self.flask_app.blueprints


    @with_context
    def test_view_renders_at_expected_route(self):
        res = self.app.get('/data', follow_redirects=True)

        assert res.status_code == 200
