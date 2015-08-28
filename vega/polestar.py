import os
import json
import cgi
import codecs

from IPython import display


JS = ['polestar/scripts/vendor-13742e93f0.js', 'polestar/scripts/app-512c772610.js']
CSS = ['polestar/styles/app-a696a065c6.css', 'polestar/scripts/vendor-e4b58aff85.css']
TEAMPLATE = 'index.html'

IFRAME_STYLE = 'border: none; width: 100%; min-height: 580px;'


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
        with codecs.open(abs_path, encoding='utf-8') as f:
            return path, f.read()

    def __styles(self, paths):
        out = []
        for p in paths:
            path, body = self.__get_content(p)
            out.append(u'<style>/*# sourceURL={path} */\n{body}</style>'.format(
                path=path, body=body))
        return u'\n'.join(out)

    def __scripts(self, paths):
        out = []
        for p in paths:
            path, body = self.__get_content(p)
            out.append((u'<script type="text/javascript">//@ sourceURL={path}'
                       '\n{body}</script>').format(path=path, body=body))
        return u'\n'.join(out)

    def __data(self):
        return self.data.tolist()

    def __escape(self, body):
        return cgi.escape(body, quote=True)

    def _repr_html_(self):
        """Used by the frontend to show html for polestar."""
        _, template = self.__get_content(TEAMPLATE)
        body = template.format(
            styles=self.__styles(CSS),
            scripts=self.__scripts(JS),
            data=json.dumps(self.__data()))
        output = u'<iframe srcdoc="{srcdoc}" style="{style}"></iframe>'.format(
            srcdoc=self.__escape(body), style=IFRAME_STYLE)
        return output
