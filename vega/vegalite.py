from __future__ import absolute_import

import json
import uuid

from IPython.display import display, display_javascript, display_html

from . import utils

JS_TEMPLATE = "static/vega-lite.js"
HTML_TEMPLATE = "static/vega-lite.html"

DEFAULTS = {
    "config": {
        "cell": {
            "width": 500,
            "height": 350
        }
    }
}


def view(spec, data=None):
    spec = prepare_spec(spec, data)
    display(VegaLite(spec))


def view(dataframe, spec={}):
    """Create and immediately display even if it is not the last line."""
    display(create(dataframe, spec))


def create(dataframe, spec={}):
    """Create vega-lite from a dataframe."""
    return VegaLite(dataframe.columns, dataframe.values, spec)


class VegaLite(object):
    """Define Vega-Lite widget."""

    def __init__(self, spec):
        self.spec = utils.update(spec, DEFAULTS, overwrite=False)

    def _generate_html(self, id):
        template = utils.get_content(HTML_TEMPLATE)
        return template.format(id=id)

    def _generate_js(self, id):
        template = utils.get_content(JS_TEMPLATE)
        selector = '#{0}'.format(id)
        payload = template.format(
            selector=selector,
            spec=json.dumps(self.spec),
            type='vega-lite'
        )
        return payload

    def _ipython_display_(self):
        """Used by the frontend to show html."""
        id = uuid.uuid4()
        print(self._generate_html(id))
        print(self._generate_js(id))
