# -*- coding: utf8 -*-

import sys
import os
import libcrowds_data as plugin


# Use the PyBossa test suite
sys.path.append(os.path.abspath("./pybossa/test"))

from default import with_context
from helper import web
from factories import ProjectFactory, TaskFactory, TaskRunFactory


def setUpPackage():
    """Setup the plugin."""
    from default import flask_app
    with flask_app.app_context():
        plugin_dir = os.path.dirname(plugin.__file__)
        plugin.LibCrowdsData(plugin_dir).setup()


class TestPlugin(web.Helper):

    def setUp(self):
        super(TestPlugin, self).setUp()
        self.project = ProjectFactory.create()
        self.task = TaskFactory.create(n_answers=1, state='completed')

    def test_blueprint_registered(self):
        assert 'data' in self.flask_app.blueprints

    def test_static_folder_exists(self):
        bp = self.flask_app.blueprints['data']
        static_folder = os.path.abspath(bp.static_folder)
        assert os.path.isdir(static_folder), static_folder

    def test_templates_folder_exists(self):
        bp = self.flask_app.blueprints['data']
        template_folder = os.path.abspath(bp.template_folder)
        assert os.path.isdir(template_folder), template_folder

    @with_context
    def test_view_renders_at_expected_route(self):
        res = self.app.get('/data', follow_redirects=True)
        assert res.status_code == 200

    @with_context
    def test_csv_file_exported(self):
        url = u'/{0}/csv_eport'.format(self.project.short_name)
        res = self.app.get(url, follow_redirects=True)
        content = res.headers['Content-Disposition']
        content_type = res.headers['Content-Type']
        fn = "{0}_results.csv".format(self.project.short_name)
        assert fn in content and "text/csv" in content_type


    @with_context
    @patch('libcrowds_data.view.UnicodeWriter.writerow')
    def test_populated_results_written_to_csv(self, mock_writer, mock_filter):
        TaskRunFactory.create(project=self.project, task=self.task,
                              info={'n': 1})
        url = u'/{0}/csv_eport'.format(self.project.short_name)
        res = self.app.get(url, follow_redirects=True)

        headers = mock_writer.call_args_list[0][0][0]
        row = mock_writer.call_args_list[1][0][0]

        assert headers == ['task_id']
        assert row == [self.task_id]
