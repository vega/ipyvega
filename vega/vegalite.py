from IPython import display

from tool import Tool

JS = ['../static/vega-lite/bower_components/d3/d3.js',
      '../static/vega-lite/bower_components/vega/vega.js',
      '../static/vega-lite/vega-lite.js',
      '../static/vega-lite/bower_components/vega-embed/vega-embed.js',
      '../static/embed.js']
CSS = ['../static/embed.css']
TEMPLATE = '../static/vega-lite.html'


def explore(dataframe, spec={}):
    """Create and immediately display even if it is not the last line."""
    display.display(create(dataframe, spec))


def create(dataframe, spec={}):
    """Creates vega-lite from a dataframe"""
    return VegaLite(dataframe.columns, dataframe.values, spec)


class VegaLite(Tool):
    """Defines Vega-Lite widget"""

    def __init__(self, columns, data, spec={}):
        """Constructor

        Args:
            columns: a list of column names
            data: list of rows
            spec: the initial vega-lite spec as a python dictionary"""

        super(VegaLite, self).__init__(columns, data, JS, CSS, TEMPLATE)
        self.spec = spec
