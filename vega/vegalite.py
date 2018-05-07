from __future__ import absolute_import

from .base import VegaBase
from .utils import prepare_spec


class VegaLite(VegaBase):
    """Display a Vega-Lite visualization in the Jupyter Notebook."""

    render_type = 'vega-lite'

    def _prepare_spec(self, spec, data):
        return prepare_spec(spec, data)


def entry_point_renderer(spec, embed_options=None):
    vl = VegaLite(spec, opt=embed_options)
    vl.display()
    return {'text/plain': ''}


__all__ = ['VegaLite', 'entry_point_renderer']
