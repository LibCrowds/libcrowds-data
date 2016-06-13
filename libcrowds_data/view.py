# -*- coding: utf8 -*-
"""Views modules for libcrowds-data."""

import StringIO
from flask import render_template, make_response
from pybossa.core import project_repo, result_repo
from pybossa.util import UnicodeWriter
from pybossa.exporter import Exporter
from werkzeug.utils import secure_filename


def index():
    """Return the Data page."""
    projects = [p for p in project_repo.filter_by(published=True)
                if not p.needs_password()]
    title = "Data"
    description = """Download open datasets of all crowdsourced data produced
                  via LibCrowds."""
    return render_template('/index.html', projects=projects)


def csv_export(short_name):
    """Export project results as a CSV file.

    :param short_name: The short name of the project.
    """
    project = project_repo.get_by_shortname(short_name)
    if project is None:  # pragma: no cover
        abort(404)

    si = StringIO.StringIO()
    writer = UnicodeWriter(si)
    exporter = Exporter()
    name = exporter._project_name_latin_encoded(project)
    secure_name = secure_filename('{0}_{1}.csv'.format(name, 'results'))
    results = result_repo.filter_by(project_id=project.id)
    if len(results) > 0:
        keys = [r.info.keys() for r in results if isinstance(r.info, dict)]
        headers = results[0].dictize().keys()
        headers += list(set(list(itertools.chain(*keys))))
        writer.writerow([h for h in headers])

        for row in results:
            values = results[0].dictize().items()
            if isinstance(row.info, dict):
                values.extend([row.info.get(h, '') for h in headers])
            writer.writerow(values)

    fn = "filename={0}".format(secure_name)
    resp = make_response(si.getvalue())
    resp.headers["Content-Disposition"] = "attachment; {0}".format(fn)
    resp.headers["Content-type"] = "text/csv"
    resp.headers['Cache-Control'] = "no-store, no-cache, must-revalidate, \
                                    post-check=0, pre-check=0, max-age=0"
    return resp
