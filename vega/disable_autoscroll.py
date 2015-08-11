"""
Usage:
    %load_ext vega.disable_autoscroll
"""

from IPython.display import display, Javascript

DISABLE_SCROLLING = """
IPython.OutputArea.prototype._should_scroll = function(lines) {
    return false;
}
"""


def load_ipython_extension(ip):
    display(Javascript(DISABLE_SCROLLING))
    print ("autoscrolling is disabled")
