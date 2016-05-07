from __future__ import absolute_import

from warnings import warn


def _jupyter_server_extension_paths():
    return [{
        "module": "vega"
    }]


# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        # the path is relative to the `vega` directory
        src="static",
        # directory in the `nbextension/` namespace
        dest="vega",
        # _also_ in the `nbextension/` namespace
        require="vega/index")]


def find_static_assets():
    warn("""To use the vega nbextension, you'll need to update
    the Jupyter notebook to version 4.2 or later.""")
    return []
