from IPython.display import display, Javascript, HTML

import json
import os

import utils

JS = ["../static/d3.min.js",
      "../static/vega.min.js",
      "../static/vega-lite.min.js",
      "../static/vega-embed.min.js",
      "../static/embed.js"]

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

        display(HTML(utils.styles(CSS)))
        display(HTML(utils.scripts(JS)))

        return template.format(spec=json.dumps(self.spec))

