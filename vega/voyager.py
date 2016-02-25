from IPython import display

from tool import Tool

JS = ['../static/voyager/scripts/vendor.js',
      '../static/voyager/scripts/app.js']
CSS = ['../static/voyager/styles/vendor.css',
       '../static/voyager/styles/app.css']
TEMPLATE = '../static/voyager.html'


def explore(dataframe):
    """Create and immediately display even if it is not the last line."""
    display.display(create(dataframe))


def create(dataframe):
    """Creates voyager from a dataframe"""
    return Voyager(dataframe.columns, dataframe.values)


class Voyager(Tool):
    """Defines Voyager widget"""

    def __init__(self, columns, data, spec={}):
        """Constructor

        Args:
            columns: a list of column names
            data: list of rows"""

        super(Voyager, self).__init__(columns, data, JS, CSS, TEMPLATE)
