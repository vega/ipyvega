from __future__ import absolute_import

import json
import uuid
import copy

from IPython.display import display, publish_display_data

from . import utils


class VegaBase(object):
    """A custom Vega-Lite display object."""

    JS_TEMPLATE = "static/vega.js"
    render_type = ''  # vega or vega-lite

    def __init__(self, spec, data=None, opt=None):
        """Initialize the visualization object."""
        spec = spec
        self.opt = opt or {}
        self.spec = self._prepare_spec(spec, data)

    def _prepare_spec(self, spec, data):
        return spec

    def _generate_js(self, id, **kwds):
        template = utils.get_content(self.JS_TEMPLATE)
        payload = template.format(
            id=id,
            spec=json.dumps(self.spec, **kwds),
            opt=json.dumps(self.opt, **kwds),
            type=self.render_type
        )
        return payload

    def _repr_mimebundle_(self, include=None, exclude=None):
        """Display the visualization in the Jupyter notebook."""
        id = uuid.uuid4()
        return (
            {'application/javascript': self._generate_js(id)},
            {'jupyter-vega': '#{0}'.format(id)},
        )

    def display(self):
        """Render the visualization."""
        display(self)
