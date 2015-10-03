from IPython import display

from tool import Tool

JS = ['../static/vegalite/scripts/vendor.js',
      '../static/vegalite/scripts/app.js']
CSS = ['../static/vegalite/styles/custom.css']
TEMPLATE = '../static/vegalite.html'


def explore(dataframe, spec={}):
    """Create and immediately display even if it is not the last line."""
    display.display(create(dataframe, spec))


def create(dataframe, spec={}):
    """Creates vegalite from a dataframe"""
    return Vegalite(dataframe.columns, dataframe.values, spec)


class Vegalite(Tool):
    """Defines Vegalite widget"""

    def __init__(self, columns, data, spec={}):
        """Constructor

        Args:
            columns: a list of column names
            data: list of rows
            spec: the initial vega-lite spec as a python dictionary"""

        super(Vegalite, self).__init__(columns, data, JS, CSS, TEMPLATE)
        self.spec = spec
