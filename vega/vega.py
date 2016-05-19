from __future__ import absolute_import

from .base import VegaBase


DEFAULTS = {}


class Vega(VegaBase):
    """Display a Vega visualization in the Jupyter Notebook."""

    DEFAULTS = DEFAULTS
    render_type = 'vega'


__all__ = ['Vega']
