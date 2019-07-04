from __future__ import absolute_import

from warnings import warn

from .vega import Vega
from .vegalite import VegaLite


__all__ = ['Vega', 'VegaLite']

__version__ = '2.4.0'


def _jupyter_nbextension_paths():
    """Return metadata for the jupyter-vega nbextension."""
    return [dict(
        section="notebook",
        # the path is relative to the `vega` directory
        src="static",
        # directory in the `nbextension/` namespace
        dest="jupyter-vega",
        # _also_ in the `nbextension/` namespace
        require="jupyter-vega/index")]


def find_static_assets():
    warn("""To use the vega nbextension, you'll need to update
    the Jupyter notebook to version 4.2 or later.""")
    return []
