# -*- coding: utf8 -*-

import sys
import os
import libcrowds_data as plugin
from xml.dom.minidom import parseString
from mock import patch


# Use the PyBossa test suite
sys.path.append(os.path.abspath("./pybossa/test"))

from default import with_context
from helper import web
from factories import ProjectFactory, TaskFactory, TaskRunFactory
from pybossa.core import result_repo


def setUpPackage():
    """Setup the plugin."""
    from default import flask_app
    with flask_app.app_context():
        plugin_dir = os.path.dirname(plugin.__file__)
        plugin.LibCrowdsData(plugin_dir).setup()


class TestPlugin(web.Helper):

    def setUp(self):
        super(TestPlugin, self).setUp()
        self.project = ProjectFactory.create(short_name='project')
        self.task = TaskFactory.create(n_answers=1, state='completed')

    @with_context
    def test_get_main_view(self):
        res = self.app.get('/data', follow_redirects=True)
        assert res.status_code == 200, res.status_code

    @with_context
    def test_get_csv_export_view(self):
        res = self.app.get('/data/project/csv_export', follow_redirects=True)
        assert res.status_code == 200, res.status_code

    @with_context
    def test_get_xml_export_view(self):
        res = self.app.get('/data/project/xml_export', follow_redirects=True)
        assert res.status_code == 200, res.status_code

    @with_context
    def test_csv_file_exported(self):
        self.signin(email='owner@a.com', password='1234')
        res = self.app.get('/data/project/csv_export', follow_redirects=True)
        content = res.headers['Content-Disposition']
        content_type = res.headers['Content-Type']
        fn = "{0}_results.csv".format(self.project.short_name)
        assert fn in content, content
        assert "text/csv" in content_type, content_type

    @with_context
    def test_xml_file_exported(self):
        self.signin(email='owner@a.com', password='1234')
        res = self.app.get('/data/project/xml_export', follow_redirects=True)
        content = res.headers['Content-Disposition']
        content_type = res.headers['Content-Type']
        fn = "{0}_results.xml".format(self.project.short_name)
        assert fn in content, content
        assert "text/xml" in content_type, content_type

    @with_context
    @patch('libcrowds_data.view.UnicodeWriter.writerow')
    def test_correct_data_written_to_csv(self, mock_writer):
        TaskRunFactory.create(project=self.project, task=self.task)
        result = result_repo.filter_by(project_id=self.project.id)[0]
        result.info = {'n': 42}
        result_repo.update(result)
        res = self.app.get('/data/project/csv_export', follow_redirects=True)
        expected_headers = ['info', 'task_id', 'created', 'last_version',
                            'task_run_ids', 'project_id', 'id', 'info_n']
        expected_row = result.dictize().values() + [42]
        headers = mock_writer.call_args_list[0][0][0]
        row = mock_writer.call_args_list[1][0][0]
        assert sorted(headers) == sorted(expected_headers)
        assert sorted(row) == sorted(expected_row)

    @with_context
    def test_correct_data_written_to_xml(self):
        TaskRunFactory.create(project=self.project, task=self.task)
        result = result_repo.filter_by(project_id=self.project.id)[0]
        result.info = {'n': 42}
        result_repo.update(result)
        resp = self.app.get('/data/project/xml_export', follow_redirects=True)
        xml = ('<?xml version="1.0" encoding="UTF-8" ?><record-group>'
               '<record><n>42</n></record></record-group>')
        dom = parseString(xml)
        expected = dom.toprettyxml()
        assert resp.data == expected, resp.data
