import json
import os

import numpy as np
import pandas as pd

from ..utils import sanitize_dataframe, nested_update, abs_path


def test_nested_update():
    D = {'A': {'a': 4, 'b': 5}}
    U = {'A': {'a': 40, 'c': 6}, 'B':{'foo': 'bar'}}
    output = nested_update(D, U)
    assert output is D
    assert D == {'A': {'a': 40, 'b': 5, 'c': 6}, 'B':{'foo': 'bar'}}


def test_sanitize_dataframe():
    # create a dataframe with various types
    df = pd.DataFrame({'s': list('abcde'),
                       'f': np.arange(5, dtype=float),
                       'i': np.arange(5, dtype=int),
                       'd': pd.date_range('2012-01-01', periods=5, freq='H'),
                       'c': pd.Series(list('ababc'), dtype='category')})

    # add some nulls
    df.ix[0, 's'] = None
    df.ix[0, 'f'] = np.nan
    df.ix[0, 'd'] = pd.NaT

    # JSON serialize. This will fail on non-sanitized dataframes
    df_clean = sanitize_dataframe(df)
    s = json.dumps(df_clean.to_dict(orient='records'))

    # Re-construct pandas dataframe
    df2 = pd.read_json(s)

    # Re-apply original types
    for col in df:
        if str(df[col].dtype).startswith('datetime'):
            # astype(datetime) introduces time-zone issues:
            # to_datetime() does not.
            df2[col] = pd.to_datetime(df2[col])
        else:
            df2[col] = df2[col].astype(df[col].dtype)

    assert df.equals(df2)
