import cgi
import codecs
import collections
import os.path
import copy


def update(d, u, overwrite=True):
    """Update dictionary.

    If overwrite is False, then existing keys in d won't be overwritten
    by values in u.
    """
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


def escape(string):
    """Escape the string."""
    return cgi.escape(string, quote=True)


def sanitize_dataframe(df):
    """Sanitize a DataFrame to prepare it for serialization.

    * Make a copy.
    * Raise ValueError if it has a hierarchical index.
    * Convert categoricals to strings.
    * Convert datetimes to strings.
    * Convert floats to objects and replace NaNs by None.
    """
    import pandas as pd
    df = df.copy()

    if isinstance(df.index, pd.core.index.MultiIndex):
        raise ValueError('Hierarchical indices not supported')
    if isinstance(df.columns, pd.core.index.MultiIndex):
        raise ValueError('Hierarchical indices not supported')

    for col_name, dtype in df.dtypes.iteritems():
        if str(dtype) == 'category':
            # XXXX: work around bug in to_json for categorical types
            # https://github.com/pydata/pandas/issues/10778
            df[col_name] = df[col_name].astype(str)
        if str(dtype).startswith('datetime'):
            # Convert datetimes to strings
            df[col_name] = df[col_name].astype(str).replace('NaT', '')
        if str(dtype).startswith('float'):
            # For floats, convert nan->None
            s = df[col_name].astype(object)
            df[col_name] = s.where(s.notnull(), None)
    return df


def prepare_spec(spec, data=None):
    """Prepare a Vega-Lite spec for sending to the frontend.

    This allows data to be passed in either as part of the spec
    or separately. If separately, the data is assumed to be a
    pandas DataFrame or object that can be converted to to a DataFrame.
    """
    import pandas as pd

    if isinstance(data, pd.DataFrame):
        # We have to do the isinstance test first because we can't
        # compare a DataFrame to None.
        spec = copy.deepcopy(spec)
        data = sanitize_dataframe(data)
        spec['data'] = {'values': data.to_dict(orient='records')}
    elif data is None:
        # Data is either passed in spec or error
        if 'data' not in spec:
            raise ValueError('No data provided')
    else:
        # As a last resort try to pass the data to a DataFrame and use it
        data = pd.DataFrame(data)
        spec = copy.deepcopy(spec)
        data = sanitize_dataframe(data)
        spec['data'] = {'values': data.to_dict(orient='records')}
    return spec
