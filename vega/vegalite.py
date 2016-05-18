from __future__ import absolute_import

from IPython.display import display, publish_display_data

from .base import VegaBase
from .utils import prepare_spec


DEFAULTS = {
    "config": {
        "cell": {
            "width": 500,
            "height": 350
        }
    }
}


class VegaLite(VegaBase):
    """Display a Vega-Lite visualization in the Jupyter Notebook."""

    DEFAULTS = DEFAULTS
    render_type = 'vega-lite'

    def _prepare_spec(self, spec, data):
        return prepare_spec(spec, data)


__all__ = ['VegaLite']
