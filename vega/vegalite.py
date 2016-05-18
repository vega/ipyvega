from __future__ import absolute_import

import json
import uuid

from IPython.display import display, publish_display_data

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
    """View a Vega-Lite visualization in the Jupyter notebook.
    
    Parameters
    ----------
    spec : dict
        The Vega-Lite spec as a Python dict.
    data : pandas.DataFrame
        If the spec doesn't encode the data, it can be passed in separately.
    """
    spec = utils.prepare_spec(spec, data)
    display(VegaLite(spec))


def create(spec, data=None):
    """Create Vega-Lite visualization from a spec and (optionaly) data.
    
    Parameters
    ----------
    spec : dict
        The Vega-Lite spec as a Python dict.
    data : pandas.DataFrame
        If the spec doesn't encode the data, it can be passed in separately.
    """
    return VegaLite(spec)


class VegaLite(object):
    """A custom Vega-Lite display object."""

    def __init__(self, spec):
        if 'data' not in spec:
            raise KeyError('No data provided with spec')
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
        """Display the visualization in the Jupyter notebook."""
        id = uuid.uuid4()
        publish_display_data(
            {'text/html':self._generate_html(id)},
            metadata={'jupyter-vega': '#{0}'.format(id)}
        )
        publish_display_data(
            {'application/javascript': self._generate_js(id)},
            metadata={'jupyter-vega': '#{0}'.format(id)}
        )
        
