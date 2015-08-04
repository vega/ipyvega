from IPython import display


def get_object_id(o):
    return object.__repr__(o).split()[3][1:-1]


def create(dataframe):
    """Creates polestar from a dataframe"""
    return Polestar(dataframe.columns, dataframe.values)


class Polestar(display.DisplayObject):
    """Defines Polestar widget"""

    def __init__(self, columns, data):
        """Constructor

        Args:
            columns: a list of column names

            data: list of rows"""

        self.id = 'PS_' + get_object_id(self)
        self.data = data
        self.columns = columns

    def _repr_html_(self):
        """Used by the frontend to show html for polestar."""
        return '<strong>Polstar</strong> with {} columns and {} rows.'.format(
            len(self.columns), len(self.data))
