from __future__ import absolute_import

import json

from IPython.display import display

from . import utils


TEMPLATE = "static/vega.html"


def view(spec):
    """Create and immediately display even if it is not the last line."""
    display(create(spec))


def create(spec):
    """Creates vega from a dataframe"""
    return Vega(spec)


class Vega(object):
    """Defines Vega widget"""

    def __init__(self, spec):
        self.spec = spec

    def _repr_html_(self):
        """Used by the frontend to show html."""
        template = utils.get_content(TEMPLATE)

        return template.format(spec=json.dumps(self.spec))
