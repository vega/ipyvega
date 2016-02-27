import os.path
import cgi
import json
import codecs
import collections


def update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def require(script):
    wrapped = "{}".format(script)

    return wrapped


def script(path):
    return (u'<script type="text/javascript" charset="utf-8">//@ sourceURL={path}'
                     '\n{body}</script>').format(
                        path=os.path.basename(path),
                        body=require(get_content(path)))


def scripts(paths):
    """ Generate script tags for the given path """
    out = []
    for path in paths:
        out.append(script(path))
    return u'\n'.join(out)


def abs_path(path):
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        path)


def get_content(path):
    """ Get content of file """
    with codecs.open(abs_path(path), encoding='utf-8') as f:
        return f.read()


def styles(paths):
    """ Generate inline style tags for the files in the given paths """
    out = []
    for path in paths:
        out.append(
            u'<style>/*# sourceURL={path} */\n{body}</style>'.format(
                path=os.path.basename(path),
                body=get_content(path)))
    return u'\n'.join(out)


def data(data, columns):
    """ Creates a dictionary from a pandas data frame """
    res = []
    for row in data.tolist():
        res.append({k: v for k, v in zip(columns, row)})
    return res


def escape(string):
    """ Escape the string """
    return cgi.escape(string, quote=True)