import os.path
import cgi
import json
import codecs

IFRAME_STYLE = 'border: none; width: 100%; min-height: 580px;'

IFRAME = u'<iframe sandbox="allow-scripts" srcdoc="{srcdoc}" style="{style}"></iframe>'


class Tool(object):
    """Abstract class for polestar and voyager widget"""

    def __init__(self, columns, data, js, css, template):
        """Constructor

        Args:
            columns: a list of column names
            data: list of rows
            js: list of js file paths
            css: list of css file paths
            template: path to html template"""

        self.data = data
        self.columns = columns

        self._js = js
        self._css = css
        self._template = template

    def __get_content(self, path):
        abs_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            path)
        with codecs.open(abs_path, encoding='utf-8') as f:
            return f.read()

    def __styles(self, paths):
        out = []
        for path in paths:
            out.append(
                u'<style>/*# sourceURL={path} */\n{body}</style>'.format(
                    path=os.path.basename(path),
                    body=self.__get_content(path)))
        return u'\n'.join(out)

    def __scripts(self, paths):
        out = []
        for path in paths:
            out.append((u'<script type="text/javascript" charset="utf-8">//@ sourceURL={path}'
                       '\n{body}</script>').format(
                       path=os.path.basename(path),
                       body=self.__get_content(path)))
        return u'\n'.join(out)

    def __data(self):
        res = []
        for row in self.data.tolist():
            res.append({k: v for k, v in zip(self.columns, row)})
        return res

    def __escape(self, body):
        return cgi.escape(body, quote=True)

    def _repr_html_(self):
        """Used by the frontend to show html for polestar."""
        template = self.__get_content(self._template)
        if hasattr(self, 'spec'):
            body = template.format(
                styles=self.__styles(self._css),
                scripts=self.__scripts(self._js),
                spec=json.dumps(self.spec),
                data=json.dumps(self.__data()))
        else:
            body = template.format(
                styles=self.__styles(self._css),
                scripts=self.__scripts(self._js),
                data=json.dumps(self.__data()))
        output = IFRAME.format(
            srcdoc=self.__escape(body), style=IFRAME_STYLE)
        return output
