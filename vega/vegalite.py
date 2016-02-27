from IPython.display import display, Javascript, HTML
from IPython.html import install_nbextension

import json
import os

from . import __path__
import utils

JS = ["../static/d3.min.js",
      "../static/vega.min.js",
      "../static/vega-lite.min.js",
      "../static/vega-embed.min.js"]

EMBED = "../static/embed.js"

CSS = ["../static/embed.css"]

TEMPLATE = "../static/vega-lite.html"

DEFAULTS = {
    "config": {
        "cell": {
            "width": 500,
            "height": 350
        }
    }
}

def install():
    display(HTML(utils.styles(CSS)))
    for path in JS:
        install_nbextension(utils.abs_path(path))
    display(HTML(utils.script(EMBED) % {"path": "/notebooks/static"}))


def view(dataframe, spec={}):
    """Create and immediately display even if it is not the last line."""
    display(create(dataframe, spec))


def create(dataframe, spec={}):
    """Creates vega-lite from a dataframe"""
    return VegaLite(dataframe.columns, dataframe.values, spec)


class VegaLite(object):
    """Defines Vega-Lite widget"""

    def __init__(self, columns, data, spec):
        self.columns = columns

        updated = utils.update(DEFAULTS, spec)

        self.spec = utils.update({
            "data": {
                "values": utils.data(data, columns)
            }
        }, updated)

    def _repr_html_(self):
        """Used by the frontend to show html."""
        template = utils.get_content(TEMPLATE)

        return template.format(spec=json.dumps(self.spec))

