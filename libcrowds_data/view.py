# -*- coding: utf8 -*-
"""Views modules for libcrowds-data."""

from flask import render_template
from pybossa.core import project_repo


def index():
    """Return the Data page."""
    projects = project_repo.get_all()
    title = "Data"
    description = """Download open datasets of all crowdsourced data produced
                  via LibCrowds."""
    return render_template('/index.html', projects=projects)
