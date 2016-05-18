from __future__ import absolute_import

from IPython.display import display, publish_display_data

from .base import VegaBase


DEFAULTS = {}


class Vega(VegaBase):
    """Display a Vega visualization in the Jupyter Notebook."""

    DEFAULTS = DEFAULTS
    render_type = 'vega'


__all__ = ['Vega']
