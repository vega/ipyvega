import os
import json
import cgi

from IPython import display


JS = ['index.js']
CSS = ['main.css']
TEAMPLATE = 'index.html'

IFRAME_STYLE = 'border: none; width: 100%; height: 450px;'


def publish(dataframe):
    """Create and immediately display even if it is not the last line."""
    display.display(create(dataframe))


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

        self.data = data
        self.columns = columns

    def __get_content(self, path):
        path = os.path.join('static', path)
        abs_path = os.path.abspath(path)
        with open(abs_path, 'r') as f:
            return path, f.read()

    def __styles(self, paths):
        out = []
        for p in paths:
            path, body = self.__get_content(p)
            out.append('<style>//@ sourceURL={path}\n{body}</style>'.format(
                path=path, body=body))
        return '\n'.join(out)

    def __scripts(self, paths):
        out = []
        for p in paths:
            path, body = self.__get_content(p)
            out.append(('<script type="text/javascript">//@ sourceURL={path}'
                       '\n{body}</script>').format(path=path, body=body))
        return '\n'.join(out)

    def __data(self):
        return {
            'cols': len(self.columns),
            'rows': len(self.data)
        }

    def __escape(self, body):
        return cgi.escape(body, quote=True)

    def _repr_html_(self):
        """Used by the frontend to show html for polestar."""
        _, template = self.__get_content(TEAMPLATE)
        body = template.format(
            styles=self.__styles(CSS), scripts=self.__scripts(JS),
            data=json.dumps(self.__data()))
        output = '<iframe srcdoc="{srcdoc}" style="{style}"></iframe>'.format(
            srcdoc=self.__escape(body), style=IFRAME_STYLE)
        return output
