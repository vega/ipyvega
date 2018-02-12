from __future__ import absolute_import

from .base import VegaBase


DEFAULTS = {}


class Vega(VegaBase):
    """Display a Vega visualization in the Jupyter Notebook."""

    DEFAULTS = DEFAULTS
    render_type = 'vega'


def entry_point_renderer(spec):
    vl = Vega(spec)
    vl.display()
    return {}


__all__ = ['Vega', 'entry_point_renderer']
