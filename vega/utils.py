import cgi
import codecs
import collections
import os.path

import pandas as pd


def update(d, u, overwrite=True):
    """Update dictionary."""
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            if overwrite or k not in d:
                d[k] = u[k]
    return d


def abs_path(path):
    """Make path absolute."""
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        path)


def get_content(path):
    """Get content of file."""
    with codecs.open(abs_path(path), encoding='utf-8') as f:
        return f.read()


def sanitize(value):
    """Make sure that the data is compatible with JSON."""
    if pd.isnull(value):
        # json doesn't support nan
        return None
    return value

def sanitize_dataframe(df):
    """Sanitize a DataFrame to prepare it for serialization.
    
    * Make a copy
    * Raise ValueError is it has a hierarchical index.
    * Convert categoricals to strings.
    """
    import pandas as pd
    df = df.copy()

    if type(df.index) == pd.core.index.MultiIndex:
        raise ValueError('Hierarchical indices not supported')
    if type(df.columns) == pd.core.index.MultiIndex:
        raise ValueError('Hierarchical indices not supported')

    for col_name, dtype in df.dtypes.iteritems():
        if str(dtype) == 'category':
            # XXXX: work around bug in to_json for categorical types
            # https://github.com/pydata/pandas/issues/10778
            df[col_name] = df[col_name].astype(str)
    return df


def data(data, columns):
    """Create a dictionary from a pandas data frame."""
    res = []
    for row in data.tolist():
        res.append({k: sanitize(v) for k, v in zip(columns, row)})
    return res


def escape(string):
    """Escape the string."""
    return cgi.escape(string, quote=True)
