from IPython import display

from tool import Tool

JS = ['../static/polestar/scripts/vendor-2fda575321.js',
      '../static/polestar/scripts/app-001ebe1cd2.js']
CSS = ['../static/polestar/styles/vendor-5779b264ab.css',
       '../static/polestar/styles/app-ca269f7a84.css']
TEAMPLATE = '../static/polestar.html'


def explore(dataframe, spec={}):
    """Create and immediately display even if it is not the last line."""
    display.display(create(dataframe, spec))


def create(dataframe, spec={}):
    """Creates polestar from a dataframe"""
    return Polestar(dataframe.columns, dataframe.values, spec)


class Polestar(Tool):
    """Defines Polestar widget"""

    def __init__(self, columns, data, spec={}):
        """Constructor

        Args:
            columns: a list of column names
            data: list of rows
            spec: the initial vega-lite spec as a python dictionary"""

        super(Polestar, self).__init__(columns, data, JS, CSS, TEAMPLATE)
        self.spec = spec
