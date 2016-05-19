"""
Usage:
    %load_ext vega.disable_autoscroll
"""

from IPython.display import Javascript, display

DISABLE_SCROLLING = """
require("notebook/js/outputarea").OutputArea.prototype._should_scroll = function(lines) {
    return false;
}
"""


def load_ipython_extension(ip):
    """Disable auto scrolling."""
    display(Javascript(DISABLE_SCROLLING))
    print("autoscrolling is disabled")
