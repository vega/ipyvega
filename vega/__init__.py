from __future__ import absolute_import

from warnings import warn

from .vega import Vega
from .vegalite import VegaLite
from .dataframes.source_adapter import SourceAdapter
from .dataframes.pandas_adapter import PandasAdapter
from .dataframes.traitlets import TableType

__all__ = ['Vega', 'VegaLite', 'SourceAdapter', 'PandasAdapter', 'TableType']

__version__ = '3.5.0'


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
