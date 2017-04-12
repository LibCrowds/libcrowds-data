# -*- coding: utf8 -*-
"""Views modules for libcrowds-data."""

import StringIO
import itertools
import dicttoxml
from xml.dom.minidom import parseString
from flask import render_template, make_response, current_app, Blueprint
from flask import request
from pybossa.core import project_repo, result_repo
from pybossa.cache import projects as cached_projects
from pybossa.cache import categories as cached_cat
from pybossa.util import UnicodeWriter
from pybossa.exporter import Exporter
from werkzeug.utils import secure_filename


blueprint = Blueprint('data', __name__, template_folder='templates',
                      static_folder='static')


def get_csv_response(results):
    """Return a CSV response containing result data."""
    si = StringIO.StringIO()
    writer = UnicodeWriter(si)
    data = []
    for r in results:
        row = {k: v for k, v in r.dictize().items()}
        if isinstance(row['info'], dict):  # Explode info
            keys = row['info'].keys()
            for k in keys:
                row['info_{0}'.format(k)] = row['info'][k]
        data.append(row)
    headers = set(itertools.chain(*[row.keys() for row in data]))
    writer.writerow([h for h in headers])
    for row in data:
        writer.writerow([row.get(h, '') for h in headers])
    return make_response(si.getvalue())


def get_xml_response(results):
    """Return an XML response containing result data."""
    data = [r.info for r in results if isinstance(r.info, dict)]
    xml = dicttoxml.dicttoxml(data, custom_root='record-group',
                              item_func=lambda x: 'record', attr_type=False)
    dom = parseString(xml)
    pretty_xml = dom.toprettyxml()
    return make_response(pretty_xml)


@blueprint.route('/')
def index():
    """Return the Data page."""
    categories = cached_cat.get_all()
    projects = {}
    for c in categories:
        n_projects = cached_projects.n_count(category=c.short_name)
        projects[c.short_name] = cached_projects.get(category=c.short_name,
                                                     page=1,
                                                     per_page=n_projects)
        for p in projects[c.short_name]:
            p['n_task_runs'] = cached_projects.n_task_runs(p['id'])
            p['n_results'] = cached_projects.n_results(p['id'])

    return render_template('/index.html', projects=projects,
                           categories=categories, title="Data")


@blueprint.route('/<short_name>/results/export')
def export_results(short_name):
    """Export project results as an XML or CSV file.

    :param short_name: The short name of the project.
    """
    project = project_repo.get_by_shortname(short_name)
    if project is None:  # pragma: no cover
        abort(404)

    fmt = request.args.get('format')
    export_formats = ["xml", "csv"]
    if not fmt:
        if len(request.args) >= 1:
            abort(404)
        return redirect(url_for('.index'))

    results = result_repo.filter_by(project_id=project.id)
    if fmt not in export_formats:
        abort(415)
    elif fmt == "xml":
        resp = get_xml_response(results)
    elif fmt == "csv":
        resp = get_csv_response(results)

    exporter = Exporter()
    name = exporter._project_name_latin_encoded(project)
    secure_name = secure_filename('{0}_results.{1}'.format(name, fmt))
    fn = "filename={0}".format(secure_name)
    resp.headers["Content-Disposition"] = "attachment; {0}".format(fn)
    resp.headers["Content-type"] = "text/{0}".format(fmt)
    resp.headers['Cache-Control'] = "no-store, no-cache, must-revalidate, \
                                    post-check=0, pre-check=0, max-age=0"
    return resp
